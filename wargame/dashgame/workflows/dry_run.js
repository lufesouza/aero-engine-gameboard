// Dry run of exco_round.js with stub agents (no agent runs): node dry_run.js exco_round.js [result.json]
// Checks syntax, the step order, the schemas and the revise rule; the stub has Rolls-Royce veto in both seats and
// Boeing's operating head flag a red-line breach; the Boeing Board vetoes one item then approves the revision,
// the Rolls-Royce Board vetoes one item twice (it reverts to the default), and the CFM/GE Board review fails
// (its items revert to the default: fail closed).
const fs = require('fs')
const src = fs.readFileSync(process.argv[2], 'utf8').replace('export const meta', 'const meta')
const calls = []
const stub = (prompt, opts) => {
  calls.push(opts)
  const s = opts.schema, mk = sch => {
    if (sch.enum) return sch.enum[sch.enum.length > 1 ? 1 : 0]
    if (sch.type === 'object') return Object.fromEntries(Object.entries(sch.properties || {}).map(([k, v]) => [k, mk(v)]))
    if (sch.type === 'array') return [mk(sch.items)]
    if (sch.type === 'boolean') return opts.label.includes('veto:ops')  ? false : true
    if (sch.type === 'number') return 1
    return 'x'
  }
  const o = mk(s)
  if (opts.label === 'cfm:board:review') return Promise.resolve(null)   // a failed Board review must fail closed
  if (opts.label.includes(':board:review') || opts.label.includes(':board:confirm')) {
    // Board stub: Boeing vetoes its first item at review and approves at confirm; Rolls-Royce vetoes at both (revert)
    const m = prompt.match(/The (?:Board items|revised Board items): ([^.]*)\./)
    const items = m ? m[1].split(', ').map(x => x.split(' = ')[0]) : []
    const side = opts.label.split(':')[0], review = opts.label.includes('review')
    o.items = items.map((k, j) => ({ order_field: k, value: 'v', ground: 'g', acceptable_alternatives: [], evidence_ids: [],
      decision: (side === 'rolls_royce' || (side === 'boeing' && review)) && j === 0 ? 'veto' : 'approve' }))
  }
  if (opts.label.includes(':veto:')) {   // Rolls-Royce: binding vetoes; Boeing: a red-line flag only; the rest concur
    o.concur = !opts.label.startsWith('rolls_royce'); o.veto = { ground: 'g', evidence_ids: [], binding: true }
    o.red_line_breach = opts.label === 'boeing:veto:ops'; o.red_line = 'H5'
  }
  return Promise.resolve(o)
}
const pipeline = async (items, ...stages) => Promise.all(items.map(async (it, i) => { let r = it; for (const st of stages) { try { r = await st(r, it, i) } catch (e) { console.log('stage threw', e.message); return null } } return r }))
const parallel = async th => Promise.all(th.map(t => t().catch(() => null)))
const fn = new (Object.getPrototypeOf(async function () {}).constructor)('agent', 'pipeline', 'parallel', 'log', 'phase', 'args', src)
fn(stub, pipeline, parallel, console.log, () => {}, { run: 'dry', round: 2, year: 2035 }).then(r => {
  console.log('agents called:', calls.length, calls.map(c => c.agentType + '/' + c.phase).join(' '))
  for (const [s, x] of Object.entries(r.sides)) console.log(s, 'binding', x.binding_vetoes, 'flags', x.red_line_flags, 'revised', !!x.revision,
    '| board items', x.board_items, 'vetoed', x.board_vetoed, 'reverted', x.board_reverted, '| final', JSON.stringify(x.final_orders))
  if (process.argv[3]) fs.writeFileSync(process.argv[3], JSON.stringify(r))
}).catch(e => { console.error('FAILED', e); process.exit(1) })
