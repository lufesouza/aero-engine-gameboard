export const meta = {
  name: 'dash-exco-round',
  description: 'One dash-2050 round played by the per-executive agents: frame, test, decide, veto check, revise, per company',
  whenToUse: 'Game master only. Use a fresh run id (not the earlier dash-2050). After `DASH_RUN=<run> python3 gm.py brief N`, run with args {run: <run>, round: N, year}. Save the result with `DASH_RUN=<run> python3 exco.py save N result.json`, then `DASH_RUN=<run> python3 gm.py adjudicate N wargame/runs/<run>/orders_exco_rN.json`.',
  phases: [
    { title: 'Frame', detail: 'CEO frames the round' },
    { title: 'Test', detail: 'CFO and operating head test the frame, in parallel and independently' },
    { title: 'Decide', detail: 'CEO decides by the team rule' },
    { title: 'Veto check', detail: 'veto holders concur or veto' },
    { title: 'Revise', detail: 'CEO revises once if a binding veto stands' },
  ],
}

// args: {run: 'dash-2050-exco', round: 1, year: 2030, sides: ['boeing', ...] (optional, default all five)}
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
    company: 'Boeing', ceo: 'boeing-ortberg', cfo: 'boeing-malave', ops: 'boeing-pope',
    names: { ceo: 'Kelly Ortberg', cfo: 'Jay Malave', ops: 'Stephanie Pope' },
    rule: 'Ortberg proposes and decides. Malave is his independent check on programme estimates: he can veto any plan that fails his buffer test (the slip leg). Rates are KPI-gated: the KPI doctrine (Pope\'s seat) vetoes a 737 Rate Increase while a quality, FAA or supply-chain problem is live (the board has no injects, so it binds only if the brief reports one). Ortberg decides everything else. (teams.md §9; both vetoes are inferences from the evidence.)',
    veto: {
      cfo: { ground: 'any plan that fails your buffer test (the slip leg)', binding: true },
      ops: { ground: 'a 737 Rate Increase while the brief reports a live quality, FAA or supply-chain problem (the KPI doctrine)', binding: true },
    },
  },
  airbus: {
    company: 'Airbus', ceo: 'airbus-faury', cfo: 'airbus-toepfer', ops: 'airbus-wagner',
    names: { ceo: 'Guillaume Faury', cfo: 'Thomas Toepfer', ops: 'Lars Wagner' },
    rule: 'The CEO leads the ExCo and takes the final call. The CFO and the CEO of Commercial Aircraft hold tests, not formal vetoes: a failed test is a soft veto, which the CEO can override only when the plan is at least $1B better (ΔPV on the brief\'s grid) than the best option that passes, and the override is recorded as a Board item. The five pillars (safety, quality, integrity, compliance, security) cannot be overridden. NGSA launch, A350 Re-engine, any cancellation and Delay Tactics are Board items; assume the Board approves when the tests pass. (teams.md; the soft veto is an inference.)',
    veto: {
      cfo: { ground: 'a failed financial test: a soft veto, binding unless the CEO records an override for a plan at least $1B better than the best option that passes, as a Board item; a five-pillars breach is binding with no override', binding: 'soft' },
      ops: { ground: 'a failed industrial or programme test: a soft veto, binding unless the CEO records an override for a plan at least $1B better than the best option that passes, as a Board item; a five-pillars breach is binding with no override', binding: 'soft' },
    },
  },
  cfm: {
    company: 'CFM/GE', ceo: 'cfm-culp', cfo: 'cfm-ghai', ops: 'cfm-ali',
    names: { ceo: 'Larry Culp', cfo: 'Rahul Ghai', ops: 'Mohamed Ali' },
    rule: 'Culp proposes and decides. Ghai tests terms and capex: price/cost positive, capex within 2-3% of revenue, no number before the airframer\'s volumes are agreed. Ali tests dates: confidence from real testing, not analysis. Whether either test is a formal veto is not shown; in this game (the script\'s inference) a failed test binds unless Culp answers it with evidence. Tie-break: "safety, quality, delivery and cost, always in that order". Culp\'s red lines: a next engine needs at least 20% better fuel burn, and durability is not traded for fuel burn. The Safran gate: narrowbody price, capacity and RISE go to the partner; expect consent (inference).',
    veto: {
      cfo: { ground: 'terms or capex that fail your tests (inference: binds unless Culp answers it with evidence)', binding: 'inference' },
      ops: { ground: 'dates not backed by real testing (inference: binds unless Culp answers it with evidence)', binding: 'inference' },
    },
  },
  pratt_whitney: {
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
    expected_scenario: str, best_grid_plan_in_expected_scenario: str, premium_b: { type: 'number' }, premium_reason: str,
    objective_note: str, predictions: str, expected_pv_b: { type: 'number' },
  },
  required: ['orders', 'other_moves', 'public_statement', 'rationale', 'memo_weighing', 'expected_scenario',
    'best_grid_plan_in_expected_scenario', 'premium_b', 'premium_reason', 'objective_note', 'predictions', 'expected_pv_b'],
})
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
if (!RUN || !N || !YEAR) throw new Error('args.run, args.round and args.year are required')
if (RUN === 'dash-2050') throw new Error('use a fresh run id: dash-2050 holds the earlier game')

const js = x => '```json\n' + JSON.stringify(x, null, 1) + '\n```'
function head(side, seat, step) {
  const t = TEAMS[side]
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

async function frame(side) {
  const t = TEAMS[side]
  const p = head(side, 'ceo', 'frame') + '\n\nWrite the framing note for your ExCo: the question this round, the levers in play, the options worth testing, the red lines in force, what you ask of your CFO and of your operating head, and your initial lean. Your colleagues see only what you return here.'
  return agent(p, { label: `${side}:frame`, phase: 'Frame', agentType: t.ceo, schema: FRAME })
}

async function test(fr, side) {
  if (!fr) throw new Error(`${side}: no frame`)
  const t = TEAMS[side]
  const one = seat => {
    const extra = t.proposes === seat ? '\n\nPer the team rule you also PROPOSE the engine orders: put them in `recommended_orders` and explain them in `proposal`.' : ''
    const p = head(side, seat, 'test') + `\n\nYour CEO's framing note, passed by the game master:\n${js(fr)}\n\nTest it independently: you do not see your colleague's memo. Apply your own tests with thresholds and the grid numbers you used, give your recommended orders, and state any veto with its ground and whether the team rule makes it binding (your veto: ${t.veto[seat].ground}). Memo of at most 250 words, in your voice.` + extra
    return agent(p, { label: `${side}:test:${seat}`, phase: 'Test', agentType: t[seat], schema: testSchema(side) })
  }
  const [cfo, ops] = await parallel([() => one('cfo'), () => one('ops')])
  return { frame: fr, cfo, ops }
}

async function decide(x, side) {
  const t = TEAMS[side]
  const p = head(side, 'ceo', 'decide') + `\n\nYour framing note:\n${js(x.frame)}\n\n${t.names.cfo}'s test memo:\n${js(x.cfo)}\n\n${t.names.ops}'s test memo:\n${js(x.ops)}\n\nDecide by the team rule. Return the company's sealed orders (one value per field), other moves, the public statement, the rationale, and how you weighed each memo. Any override of a colleague's veto goes in \`overrides\` and must be allowed by the rule.`
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

log(`Round ${N} (${YEAR}), run ${RUN}: ${SIDES.join(', ')}`)
const out = await pipeline(SIDES, s => frame(s), (fr, s) => test(fr, s), (x, s) => decide(x, s), (x, s) => vetoCheck(x, s), (x, s) => revise(x, s))
const result = { run: RUN, round: N, year: YEAR, sides: {} }
SIDES.forEach((s, i) => { result.sides[s] = out[i] })
const missing = SIDES.filter((s, i) => !out[i])
if (missing.length) log(`No result for: ${missing.join(', ')} (their orders default to hold)`)
return result
