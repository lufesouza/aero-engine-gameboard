export const meta = {
  name: 'dash-exco-round',
  description: 'One dash-2050 round per company: Board guidance, then the ExCo (frame, test, decide, veto check, revise), then Board review, revise and confirm',
  whenToUse: 'Game master only. Use a fresh run id (not the earlier dash-2050). After `DASH_RUN=<run> python3 gm.py brief N`, run with args {run: <run>, round: N, year}. Save the result with `DASH_RUN=<run> python3 exco.py save N result.json`, then `DASH_RUN=<run> python3 gm.py adjudicate N wargame/runs/<run>/orders_exco_rN.json`.',
  phases: [
    { title: 'Board guidance', detail: 'the Board recommends: priorities, risk appetite, what it would approve or veto' },
    { title: 'Frame', detail: 'CEO frames the round' },
    { title: 'Test', detail: 'CFO and operating head test the frame, in parallel and independently' },
    { title: 'Decide', detail: 'CEO decides by the team rule' },
    { title: 'Veto check', detail: 'veto holders concur or veto' },
    { title: 'Revise', detail: 'CEO revises once if a binding veto or a red-line flag stands' },
    { title: 'Board review', detail: 'the Board approves or vetoes each Board item and recommends' },
    { title: 'Board revise', detail: 'CEO revises once within a Board veto' },
    { title: 'Board confirm', detail: 'the Board approves or vetoes the revised items; a still-vetoed item reverts to the default' },
  ],
}

// args: {run: 'dash-2050-exco', round: 1, year: 2030, sides: ['boeing', ...] (optional, default all five),
//        board: true (optional; false runs the ExCo alone)}
// `run` must equal the DASH_RUN that gm.py used to write the briefs, and must not be the earlier game's dash-2050.
// Each executive sees only its own company's brief and what the GM passes from its colleagues. Nothing crosses
// between companies: each company's chain is independent, and the isolation hook enforces the file side.
// Not run yet: the user asked for the agents only.

// Mirrors wargame/dashgame/rules.py ORDER_FIELDS (`python3 exco.py check` compares them).
// ORDER_FIELDS_BEGIN
const ORDER_FIELDS = {
  "boeing": {"fps": ["hold", "launch_7yr", "launch_10yr", "launch_via_embraer", "cancel"], "fps_engine_code": [null, 1, 2, 3, 4, 5, 6, 7], "rate_737": ["hold", "increase"], "re787": ["hold", "launch", "cancel"]},
  "airbus": {"ngsa": ["hold", "launch", "cancel"], "ngsa_engine_code": [null, 1, 2, 3, 4, 5, 6, 7], "rea350": ["hold", "launch", "cancel"], "delay_tactics": ["none", "bottleneck", "poaching", "both"]},
  "cfm": {"ducted": ["hold", "launch", "cancel"], "open_fan": ["hold", "launch", "cancel"], "partner_embraer": ["hold", "launch", "cancel"], "lobby_emissions": ["hold", "launch"], "genx": ["hold", "upgrade_genx9", "invest_genx", "cancel"]},
  "pratt_whitney": {"gtf2_solo": ["hold", "launch", "launch_if_selected", "cancel"], "jv_with_rr": ["hold", "commit", "withdraw"]},
  "rolls_royce": {"ultrafan_nb_solo": ["hold", "launch", "launch_if_selected", "cancel"], "jv_with_pw": ["hold", "commit", "withdraw"], "ultrafan_wb": ["hold", "launch", "cancel"], "t1000_upgrade": ["hold", "launch", "cancel"]}
}
// ORDER_FIELDS_END

// The default 2026 ExCo of each company and its decision rule (from executives/teams.md).
const TEAMS = {
  boeing: {
    board: 'boeing-board', boardName: 'the Boeing Board of Directors',
    company: 'Boeing', ceo: 'boeing-ortberg', cfo: 'boeing-malave', ops: 'boeing-pope',
    names: { ceo: 'Kelly Ortberg', cfo: 'Jay Malave', ops: 'Stephanie Pope' },
    rule: 'Ortberg proposes and decides. Malave is his independent check on programme estimates: he can veto any plan that fails his buffer test (the slip leg). Rates are KPI-gated: the KPI doctrine (Pope\'s seat) vetoes a 737 Rate Increase while a quality, FAA or supply-chain problem is live (the board has no injects, so it binds only if the brief reports one). Ortberg decides everything else. (teams.md §9; both vetoes are inferences from the evidence.)',
    veto: {
      cfo: { ground: 'any plan that fails your buffer test (the slip leg)', binding: true },
      ops: { ground: 'a 737 Rate Increase while the brief reports a live quality, FAA or supply-chain problem (the KPI doctrine)', binding: true },
    },
  },
  airbus: {
    board: 'airbus-board', boardName: 'the Airbus SE Board of Directors',
    company: 'Airbus', ceo: 'airbus-faury', cfo: 'airbus-toepfer', ops: 'airbus-wagner',
    names: { ceo: 'Guillaume Faury', cfo: 'Thomas Toepfer', ops: 'Lars Wagner' },
    rule: 'The CEO leads the ExCo and takes the final call. The CFO and the CEO of Commercial Aircraft hold tests, not formal vetoes: a failed test is a soft veto, which the CEO can override only when the plan is at least $1B better (ΔPV on the brief\'s grid) than the best option that passes, and the override is recorded as a Board item. The five pillars (safety, quality, integrity, compliance, security) cannot be overridden. NGSA launch, A350 Re-engine, any cancellation and Delay Tactics are Board items; assume the Board approves when the tests pass. (teams.md; the soft veto is an inference.)',
    veto: {
      cfo: { ground: 'a failed financial test: a soft veto, binding unless the CEO records an override for a plan at least $1B better than the best option that passes, as a Board item; a five-pillars breach is binding with no override', binding: 'soft' },
      ops: { ground: 'a failed industrial or programme test: a soft veto, binding unless the CEO records an override for a plan at least $1B better than the best option that passes, as a Board item; a five-pillars breach is binding with no override', binding: 'soft' },
    },
  },
  cfm: {
    board: 'cfm-board', boardName: 'the GE Aerospace Board of Directors (with Safran\'s consent on CFM programmes)',
    company: 'CFM/GE', ceo: 'cfm-culp', cfo: 'cfm-ghai', ops: 'cfm-ali',
    names: { ceo: 'Larry Culp', cfo: 'Rahul Ghai', ops: 'Mohamed Ali' },
    rule: 'Culp proposes and decides. Ghai tests terms and capex: price/cost positive, capex within 2-3% of revenue, no number before the airframer\'s volumes are agreed. Ali tests dates: confidence from real testing, not analysis. Whether either test is a formal veto is not shown; in this game (the script\'s inference) a failed test binds unless Culp answers it with evidence. Tie-break: "safety, quality, delivery and cost, always in that order". Culp\'s red lines: a next engine needs at least 20% better fuel burn, and durability is not traded for fuel burn. The Safran gate: narrowbody price, capacity and RISE go to the partner; expect consent (inference).',
    veto: {
      cfo: { ground: 'terms or capex that fail your tests (inference: binds unless Culp answers it with evidence)', binding: 'inference' },
      ops: { ground: 'dates not backed by real testing (inference: binds unless Culp answers it with evidence)', binding: 'inference' },
    },
  },
  pratt_whitney: {
    board: 'pratt-whitney-board', boardName: 'the RTX Board of Directors',
    company: 'Pratt & Whitney', ceo: 'pratt-whitney-calio', cfo: 'pratt-whitney-mitchill', ops: 'pratt-whitney-eddy',
    names: { ceo: 'Chris Calio', cfo: 'Neil Mitchill', ops: 'Shane Eddy' },
    rule: 'Eddy proposes the engine orders (on this board GTF2 and the Joint Venture with Rolls-Royce; an inference from the evidence); Calio frames the turn and proposes the disclosure. Every capital order passes Mitchill\'s payback and return gate; he can veto on four grounds: the dividend or the debt path, carrying an unselected engine, aggressive terms, booking upside before it is proven. Eddy can veto on technical grounds: durability not proven before entry into service, parts and capacity short of the fleet\'s needs. Calio decides, setting the safety and durability constraint first. Tie-breaks: the fleet beats a new engine; "if you miss a cycle" beats "we\'ll cross that bridge" only on visible demand; a rival\'s discount never moves the answer.',
    proposes: 'ops',
    veto: {
      cfo: { ground: 'one of your four grounds: the dividend or debt path, carrying an unselected engine, aggressive terms, booking upside before it is proven', binding: true },
      ops: { ground: 'durability not proven before entry into service, or parts and capacity short of the fleet\'s needs', binding: true },
    },
  },
  rolls_royce: {
    board: 'rolls-royce-board', boardName: 'the Rolls-Royce Holdings plc Board',
    company: 'Rolls-Royce', ceo: 'rolls-royce-erginbilgic', cfo: 'rolls-royce-mccabe', ops: 'rolls-royce-watson',
    names: { ceo: 'Tufan Erginbilgic', cfo: 'Helen McCabe', ops: 'Rob Watson' },
    rule: 'The CEO proposes and decides. Any launch and any aggressive terms need joint CEO-CFO sign-off against mid-to-high-teens hurdles. CFO vetoes: an equity raise, leverage above about 1.5x net debt to EBITDA, levering up for buybacks; in the game her real check is the hurdle and the unselected downside (inference). Civil veto: any compressed maturity, or a disclosed entry into service earlier than launch plus development time, or no support in place before entry into service. Tie-break: the CEO.',
    veto: {
      cfo: { ground: 'withholding your joint sign-off on a launch or aggressive terms (hurdle, unselected downside), or a balance-sheet veto', binding: true },
      ops: { ground: 'compressed maturity, a disclosed entry into service earlier than launch plus development time, or no support in place before entry into service', binding: true },
    },
  },
}

const str = { type: 'string' }
const strs = { type: 'array', items: { type: 'string' } }
const ordersSchema = side => ({
  type: 'object',
  properties: Object.fromEntries(Object.entries(ORDER_FIELDS[side]).map(([k, v]) => [k, { enum: v }])),
  required: Object.keys(ORDER_FIELDS[side]),
})
const FRAME = {
  type: 'object',
  properties: { question: str, situation: str, levers_in_play: strs, options_to_test: strs, red_lines: strs,
    asks_cfo: str, asks_ops: str, initial_lean: str, evidence_ids: strs },
  required: ['question', 'situation', 'levers_in_play', 'options_to_test', 'red_lines', 'asks_cfo', 'asks_ops', 'initial_lean', 'evidence_ids'],
}
const testSchema = side => ({
  type: 'object',
  properties: {
    tests: { type: 'array', items: { type: 'object', properties: { name: str, threshold: str, result: { enum: ['pass', 'fail', 'not applicable'] }, numbers: str, evidence_ids: strs }, required: ['name', 'threshold', 'result', 'numbers'] } },
    recommended_orders: ordersSchema(side),
    proposal: str,
    vetoes: { type: 'array', items: { type: 'object', properties: { plan: str, ground: str, binding: { type: 'boolean' }, evidence_ids: strs }, required: ['plan', 'ground', 'binding'] } },
    would_change_mind_if: str,
    memo: str,
  },
  required: ['tests', 'recommended_orders', 'vetoes', 'would_change_mind_if', 'memo'],
})
const decideSchema = side => ({
  type: 'object',
  properties: {
    orders: ordersSchema(side),
    other_moves: { type: 'array', items: { type: 'object', properties: { move: str, public: { type: 'boolean' }, detail: str }, required: ['move', 'public'] } },
    public_statement: str, rationale: str,
    memo_weighing: { type: 'object', properties: { cfo: str, ops: str }, required: ['cfo', 'ops'] },
    overrides: { type: 'array', items: { type: 'object', properties: { veto: str, reason: str, recorded_as: str }, required: ['veto', 'reason'] } },
    board_response: { type: 'array', items: { type: 'object', properties: { recommendation: str, response: str }, required: ['recommendation', 'response'] } },
    expected_scenario: str, best_grid_plan_in_expected_scenario: str, premium_b: { type: 'number' }, premium_reason: str,
    objective_note: str, predictions: str, expected_pv_b: { type: 'number' },
  },
  required: ['orders', 'other_moves', 'public_statement', 'rationale', 'memo_weighing', 'expected_scenario',
    'best_grid_plan_in_expected_scenario', 'premium_b', 'premium_reason', 'objective_note', 'predictions', 'expected_pv_b'],
})
const GUIDE = {
  type: 'object',
  properties: { priorities: strs, risk_appetite: str, expect_to_see: str, would_approve: strs, would_veto: strs,
    recommendations: { type: 'array', items: { type: 'object', properties: { text: str, evidence_ids: strs }, required: ['text'] } },
    evidence_ids: strs },
  required: ['priorities', 'risk_appetite', 'expect_to_see', 'would_approve', 'would_veto', 'recommendations', 'evidence_ids'],
}
const REVIEW = {
  type: 'object',
  properties: {
    items: { type: 'array', items: { type: 'object', properties: { order_field: str, value: str, decision: { enum: ['approve', 'veto'] }, ground: str,
      acceptable_alternatives: strs, evidence_ids: strs }, required: ['order_field', 'value', 'decision', 'ground'] } },
    recommendations: { type: 'array', items: { type: 'object', properties: { text: str, evidence_ids: strs }, required: ['text'] } },
    overall: { enum: ['approve', 'partial', 'veto'] }, note: str,
  },
  required: ['items', 'recommendations', 'overall', 'note'],
}
const VETO = {
  type: 'object',
  properties: { concur: { type: 'boolean' }, veto: { type: 'object', properties: { ground: str, evidence_ids: strs, binding: { type: 'boolean' } } },
    red_line_breach: { type: 'boolean' }, red_line: str, note: str },
  required: ['concur', 'red_line_breach', 'note'],
}

const A = args || {}
const RUN = A.run
const N = A.round
const YEAR = A.year
const SIDES = A.sides || Object.keys(TEAMS)
const BOARD = A.board !== false
if (!RUN || !N || !YEAR) throw new Error('args.run, args.round and args.year are required')
if (RUN === 'dash-2050') throw new Error('use a fresh run id: dash-2050 holds the earlier game')

const js = x => '```json\n' + JSON.stringify(x, null, 1) + '\n```'
function head(side, seat, step) {
  const t = TEAMS[side]
  if (seat === 'board') return headBoard(side, step)
  const dir = `/tmp/wargame-${side}/${RUN}`
  return [
    `War game run \`${RUN}\`, round ${N} (decision year ${YEAR}). Your step: **${step}**.`,
    `You are ${t.names[seat]} of ${t.company}. Follow your agent file: "Your step in each round", "Your tests", "Your vetoes and red lines", "Your voice".`,
    `Your company's run folder is \`${dir}/\` (use it instead of any other run folder your agent file names). Your brief for this round: \`${dir}/round${N}.md\`; the public rules: \`${dir}/rules.md\`.` +
      (N > 1 ? ` Earlier rounds (1 to ${N - 1}): ExCo notes in \`${dir}/exco/\` and sealed orders in \`${dir}/my_orders_r<k>.json\`.` : ' This is the first round: there are no earlier notes or orders.'),
    `Your ExCo's decision rule: ${t.rule}`,
    'Use only numbers from your brief and your own company\'s profile files. Read nothing of another company. Run no wargame.engine command.',
  ].join('\n\n')
}

function headBoard(side, step) {
  const t = TEAMS[side]
  const dir = `/tmp/wargame-${side}/${RUN}`
  return [
    `War game run \`${RUN}\`, round ${N} (decision year ${YEAR}). Your step: **${step}**.`,
    `You are ${t.boardName}. Follow your agent file: "Your step in each round", "Your culture", "Your tests", "Your veto and its limits", "Your recommendations".`,
    `Your company's run folder is \`${dir}/\`. The brief for this round: \`${dir}/round${N}.md\`; the public rules: \`${dir}/rules.md\`.` +
      (N > 1 ? ` Earlier rounds (1 to ${N - 1}): the ExCo's and your notes in \`${dir}/exco/\` and the sealed orders in \`${dir}/my_orders_r<k>.json\`.` : ' This is the first round.'),
    `The ExCo is ${t.names.ceo} (CEO), ${t.names.cfo} (CFO) and ${t.names.ops} (operating head). Its decision rule: ${t.rule}`,
    'Every order that differs from the default (hold, or none) is a Board item; an engine code rides with its launch. You approve or veto each Board item and recommend; you never originate orders, and you never veto a hold.',
    'Use only numbers from your brief and your own company\'s files. Read nothing of another company. Run no wargame.engine command.',
  ].join('\n\n')
}

// Board items: every order field that differs from its default; engine codes ride with their launch.
const DEFAULTS = Object.fromEntries(Object.entries(ORDER_FIELDS).map(([sd, f]) => [sd, Object.fromEntries(Object.entries(f).map(([k, v]) => [k, v[0]]))]))
const isCode = k => k.endsWith('_engine_code')
function boardItems(side, orders) {
  return Object.keys(ORDER_FIELDS[side]).filter(k => !isCode(k) && orders && orders[k] !== undefined && orders[k] !== DEFAULTS[side][k])
}
function revert(side, orders, fields) {
  const o = Object.assign({}, orders)
  for (const k of fields) {
    o[k] = DEFAULTS[side][k]
    const code = `${k}_engine_code`
    if (code in o) o[code] = DEFAULTS[side][code]
  }
  return o
}

async function guidance(side) {
  const t = TEAMS[side]
  if (!BOARD) return null
  const p = head(side, 'board', 'guidance') + '\n\nGive the ExCo your guidance for this round: your priorities, your risk appetite this round, what you expect to see in the package, what you would approve and what you would veto, and your recommendations. It does not bind; your veto comes at the review.'
  return agent(p, { label: `${side}:board:guidance`, phase: 'Board guidance', agentType: t.board, schema: GUIDE })
}

async function frame(side, board_guidance) {
  const t = TEAMS[side]
  const g = board_guidance ? `\n\nThe Board's guidance for this round (non-binding; its veto comes after your decision):\n${js(board_guidance)}` : ''
  const p = head(side, 'ceo', 'frame') + g + '\n\nWrite the framing note for your ExCo: the question this round, the levers in play, the options worth testing, the red lines in force, what you ask of your CFO and of your operating head, and your initial lean. Your colleagues see only what you return here.'
  const fr = await agent(p, { label: `${side}:frame`, phase: 'Frame', agentType: t.ceo, schema: FRAME })
  return fr && Object.assign({}, fr, { _board_guidance: board_guidance })
}

async function test(fr, side) {
  if (!fr) throw new Error(`${side}: no frame`)
  const t = TEAMS[side]
  const one = seat => {
    const extra = t.proposes === seat ? '\n\nPer the team rule you also PROPOSE the engine orders: put them in `recommended_orders` and explain them in `proposal`.' : ''
    const g = fr._board_guidance ? `\n\nThe Board's guidance for this round:\n${js(fr._board_guidance)}` : ''
    const frame = Object.assign({}, fr); delete frame._board_guidance
    const p = head(side, seat, 'test') + `\n\nYour CEO's framing note, passed by the game master:\n${js(frame)}${g}\n\nTest it independently: you do not see your colleague's memo. Apply your own tests with thresholds and the grid numbers you used, give your recommended orders, and state any veto with its ground and whether the team rule makes it binding (your veto: ${t.veto[seat].ground}). Memo of at most 250 words, in your voice.` + extra
    return agent(p, { label: `${side}:test:${seat}`, phase: 'Test', agentType: t[seat], schema: testSchema(side) })
  }
  const [cfo, ops] = await parallel([() => one('cfo'), () => one('ops')])
  const frame = Object.assign({}, fr); delete frame._board_guidance
  return { board_guidance: fr._board_guidance || null, frame, cfo, ops }
}

async function decide(x, side) {
  const t = TEAMS[side]
  const g = x.board_guidance ? `\n\nThe Board's guidance for this round:\n${js(x.board_guidance)}` : ''
  const br = x.board_guidance ? ' Answer each of the Board\'s recommendations in `board_response`: how you took it up, or why not. Every order that differs from the default goes to the Board, which can veto it.' : ''
  const p = head(side, 'ceo', 'decide') + `\n\nYour framing note:\n${js(x.frame)}${g}\n\n${t.names.cfo}'s test memo:\n${js(x.cfo)}\n\n${t.names.ops}'s test memo:\n${js(x.ops)}\n\nDecide by the team rule. Return the company's sealed orders (one value per field), other moves, the public statement, the rationale, and how you weighed each memo. Any override of a colleague's veto goes in \`overrides\` and must be allowed by the rule.${br}`
  const decision = await agent(p, { label: `${side}:decide`, phase: 'Decide', agentType: t.ceo, schema: decideSchema(side) })
  return Object.assign({}, x, { decision })
}

async function vetoCheck(x, side) {
  if (!x.decision) throw new Error(`${side}: no decision`)
  const t = TEAMS[side]
  const one = seat => {
    const p = head(side, seat, 'veto_check') + `\n\nYour own test memo:\n${js(x[seat])}\n\nThe CEO's decision:\n${js(x.decision)}\n\nConcur, or invoke a veto only on a ground the team rule gives you: ${t.veto[seat].ground}. Set \`veto.binding\` true only if, under the rule, the CEO must revise within it (or record an allowed override). Separately, if the orders break a company hard rule (a red line), set \`red_line_breach\` true and name the rule in \`red_line\`: that is not a veto, but the CEO must strike the breach.`
    return agent(p, { label: `${side}:veto:${seat}`, phase: 'Veto check', agentType: t[seat], schema: VETO })
  }
  const [cfo, ops] = await parallel([() => one('cfo'), () => one('ops')])
  return Object.assign({}, x, { veto_checks: { cfo, ops } })
}

async function revise(x, side) {
  const t = TEAMS[side]
  const vc = x.veto_checks
  const binding = ['cfo', 'ops'].filter(s => vc[s] && !vc[s].concur && vc[s].veto && vc[s].veto.binding)
  const flags = ['cfo', 'ops'].filter(s => vc[s] && vc[s].red_line_breach)
  if (!binding.length && !flags.length) return Object.assign({}, x, { binding_vetoes: [], red_line_flags: [], revision: null, final: x.decision })
  const parts = []
  if (binding.length) parts.push('Binding veto(es) from your ExCo:\n\n' + binding.map(s => `${t.names[s]}: ${js(vc[s])}`).join('\n\n'))
  if (flags.length) parts.push('Company red-line breach(es) flagged by your ExCo:\n\n' + flags.map(s => `${t.names[s]}: ${js({ red_line: vc[s].red_line, note: vc[s].note })}`).join('\n\n'))
  const p = head(side, 'ceo', 'revise') + `\n\nYour decision:\n${js(x.decision)}\n\n${parts.join('\n\n')}\n\nRevise your orders once. Stay within each binding veto, or override only where the team rule allows it and record each override in \`overrides\`. Strike every flagged red-line breach you confirm (red lines are never traded for PV); if you judge a flag mistaken, keep the order and say why in \`rationale\`.`
  const revision = await agent(p, { label: `${side}:revise`, phase: 'Revise', agentType: t.ceo, schema: decideSchema(side) })
  return Object.assign({}, x, { binding_vetoes: binding, red_line_flags: flags, revision, final: revision || x.decision })
}

async function boardReview(x, side) {
  const t = TEAMS[side]
  const items = boardItems(side, x.final.orders)
  if (!BOARD) return Object.assign({}, x, { board_items: items, board_review: null })
  if (!items.length) return Object.assign({}, x, { board_items: [], board_review: { items: [], recommendations: [], overall: 'approve', note: 'No Board items: every order is the default.' } })
  const pkg = { frame: x.frame, cfo_memo: x.cfo, ops_memo: x.ops, decision: x.decision, veto_checks: x.veto_checks, revision: x.revision }
  const p = head(side, 'board', 'review') + `\n\nYour guidance this round:\n${js(x.board_guidance)}\n\nThe ExCo's package, passed by the game master:\n${js(pkg)}\n\nThe orders it submits:\n${js(x.final.orders)}\n\nThe Board items: ${items.join(', ')}. For each, approve or veto, with the ground and evidence; for a veto you may name acceptable alternatives (other values of that order field, or the default). Then your recommendations.`
  const rv = await agent(p, { label: `${side}:board:review`, phase: 'Board review', agentType: t.board, schema: REVIEW })
  return Object.assign({}, x, { board_items: items, board_review: rv })
}

async function boardReviseConfirm(x, side) {
  const t = TEAMS[side]
  const rv = x.board_review
  const vetoed = rv ? rv.items.filter(i => i.decision === 'veto' && x.board_items.includes(i.order_field)).map(i => i.order_field) : []
  if (!vetoed.length) return Object.assign({}, x, { board_vetoed: [], board_revision: null, board_confirm: null, board_reverted: [], final_orders: x.final.orders })
  const p = head(side, 'ceo', 'board_revise') + `\n\nYour orders as submitted:\n${js(x.final)}\n\nThe Board's review:\n${js(rv)}\n\nThe Board vetoed: ${vetoed.join(', ')}. Revise once, within the Board's veto: for each vetoed order choose an alternative the Board named, or the default. Keep the approved orders. Answer the Board's recommendations in \`board_response\`.`
  const rev = await agent(p, { label: `${side}:board:revise`, phase: 'Board revise', agentType: t.ceo, schema: decideSchema(side) })
  let orders = rev ? Object.assign({}, x.final.orders, ...vetoed.map(k => ({ [k]: rev.orders[k] }))) : revert(side, x.final.orders, vetoed)
  if (rev) for (const k of vetoed) { const c = `${k}_engine_code`; if (c in rev.orders) orders[c] = rev.orders[c] }
  const changed = vetoed.filter(k => orders[k] !== DEFAULTS[side][k])
  let confirm = null, reverted = vetoed.filter(k => orders[k] === DEFAULTS[side][k])
  if (changed.length) {
    const cp = head(side, 'board', 'confirm') + `\n\nYou vetoed ${vetoed.join(', ')}. The CEO's revision:\n${js(rev)}\n\nThe revised Board items: ${changed.map(k => `${k} = ${orders[k]}`).join(', ')}. Approve or veto each. A still-vetoed item reverts to the default.`
    confirm = await agent(cp, { label: `${side}:board:confirm`, phase: 'Board confirm', agentType: t.board, schema: REVIEW })
    const still = confirm ? confirm.items.filter(i => i.decision === 'veto' && changed.includes(i.order_field)).map(i => i.order_field) : changed
    orders = revert(side, orders, still)
    reverted = reverted.concat(still)
  }
  return Object.assign({}, x, { board_vetoed: vetoed, board_revision: rev, board_confirm: confirm, board_reverted: reverted,
    final_orders: orders, final: Object.assign({}, rev || x.final, { orders }) })
}

log(`Round ${N} (${YEAR}), run ${RUN}: ${SIDES.join(', ')}${BOARD ? ', with the Boards' : ', ExCo only'}`)
const out = await pipeline(SIDES, s => guidance(s), (g, s) => frame(s, g), (fr, s) => test(fr, s), (x, s) => decide(x, s),
  (x, s) => vetoCheck(x, s), (x, s) => revise(x, s), (x, s) => boardReview(x, s), (x, s) => boardReviseConfirm(x, s))
const result = { run: RUN, round: N, year: YEAR, sides: {} }
SIDES.forEach((s, i) => { result.sides[s] = out[i] })
const missing = SIDES.filter((s, i) => !out[i])
if (missing.length) log(`No result for: ${missing.join(', ')} (their orders default to hold)`)
return result
