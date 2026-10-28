// Runs the original round script (wargame/dashgame/workflows/exco_round.js) with scripted seat answers instead of
// agents, for the differential test of the pack's runner (test_runner_vs_js.py).
//   node js_round.js <exco_round.js> <scenario.json>   -> prints the round result as JSON
const fs = require('fs')
const src = fs.readFileSync(process.argv[2], 'utf8').replace('export const meta =', 'const meta =')
const sc = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'))
const agent = async (prompt, opts) => {
  const k = opts.label
  if (!(k in sc.answers)) throw new Error('no scripted answer for ' + k)
  const a = sc.answers[k]
  return a === null ? null : JSON.parse(JSON.stringify(a))
}
const parallel = async thunks => Promise.all(thunks.map(t => t().catch(() => null)))
const pipeline = async (items, ...stages) => Promise.all(items.map(async (it, i) => {
  let x = it
  try { for (const st of stages) x = await st(x, it, i); return x } catch (e) { return null }
}))
const log = () => {}
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const run = new AsyncFunction('agent', 'parallel', 'pipeline', 'log', 'args', src)
run(agent, parallel, pipeline, log, sc.args).then(r => console.log(JSON.stringify(r))).catch(e => { console.error(e); process.exit(1) })
