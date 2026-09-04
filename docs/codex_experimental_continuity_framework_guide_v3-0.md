# Codex Experimental Continuity Framework Guide v3.0

긴 실험 작업을 여러 세션으로 나눠도 장기 목표와 실험 판단이 끊기지 않게 하는 최소 프레임

## 1. 해결하려는 문제

이 프레임의 기본 목적은 범용 AI 소프트웨어 개발 운영체제를 만드는 것이 아니다.

해결하려는 문제는 다음과 같다.

> 긴 실험 작업을 여러 세션으로 쪼개도 Codex가 장기 목표, 실험 기준, 현재 가설, 이미 배운 실패를 잊지 않고 다음 작업을 이어가게 한다.

백테스트나 모델 실험처럼 반복 횟수가 많은 작업에서는 다음 drift가 쉽게 생긴다.

```text
원래 목표
  -> 가설 실험
  -> 성과 부족
  -> 파라미터 조정
  -> 다른 metric 개선
  -> 아이디어와 scope 추가
  -> 원래 목적 상실
```

이는 단순한 대화 memory 부족보다 `goal drift + experimental discipline` 문제에 가깝다. 따라서 compact나 대규모 지식 시스템보다, 세션마다 다시 주입해야 할 정보를 종류별로 분리하는 것이 우선이다.

## 2. 두 단계 원칙

프레임은 실제로 관측된 실패 때문에 성장한다.

```text
Level 1 — Continuity
GOAL + active state + experiment ledger + drift review
              |
              | 코드 위치·ownership 문제가 반복될 때만
              v
Level 2 — Architecture
ARCHITECTURE + domain memory + Steward + local AGENTS + custom roles
```

Level 1이 기본 설치다. Level 2는 큰 프로젝트라서 자동으로 설치하는 것이 아니라, Codex가 코드 위치나 경계를 반복해서 틀리는 증거가 생겼을 때 선택한다.

## 3. Level 1의 네 파일군

```text
repo/
├── AGENTS.md
├── GOAL.md
├── state/
│   └── active/
│       └── <task>.md
└── memory/
    └── experiments.md
```

프레임 번들에는 `<task>.md`를 만들기 위한 `state/active/_template.md`가 들어 있다. 프로젝트에 실제로 필요한 operational artifact는 위 네 종류다.

## 4. AGENTS.md — 최초 전파 노드

Codex는 작업 전에 적용되는 `AGENTS.md`를 읽는다. 공식 문서에 따르면 프로젝트 루트에서 현재 작업 디렉터리까지 지침을 합치며, 더 가까운 파일이 뒤에 적용된다.

- https://learn.chatgpt.com/docs/agent-configuration/agents-md

Level 1의 루트 `AGENTS.md`는 모든 판단을 대신하는 거대한 orchestration 문서가 아니다. 세션이 같은 기준점에서 출발하도록 다음 순서를 전파한다.

1. `GOAL.md`를 읽는다.
2. 관련 active state를 읽는다.
3. 관련 experiment memory를 읽는다.
4. 이번 작업과 목표 criterion의 연결을 명시한다.
5. 최소 실험이나 구현을 수행한다.
6. 결과, 해석, 판단, 다음 행동을 active state에 남긴다.
7. 장기적으로 반복을 막는 교훈만 ledger에 남긴다.
8. trigger가 충족되면 drift review를 실행한다.

새 코드를 만들 때는 최소한의 cohesive module과 명시적인 input/output을 사용한다. 다만 Level 1은 ownership map이나 architecture governance를 미리 만들지 않는다.

## 5. GOAL.md — 사용자 소유의 기준점

`GOAL.md`는 가장 중요한 파일이며 사용자가 소유한다. Codex는 명시적인 사용자 요청 없이 수정하지 않는다.

포함할 내용은 다음과 같다.

- 실제 장기 목적
- 성공을 함께 구성하는 평가 기준
- 훼손하면 안 되는 guardrail
- 최적화하면 안 되는 proxy와 shortcut
- 중단, 기각, 재검토 조건
- 현재 핵심 가설
- 결과 비교에 필요한 고정 평가 가정

백테스트 프로젝트에서는 dataset과 IS/OOS split, transaction cost, slippage, baseline, metric 정의가 바뀌면 결과 비교가 무너질 수 있다. 이런 조건은 `Fixed Evaluation Assumptions`에 둔다.

새 evidence가 GOAL 변경을 시사해도 agent가 자동으로 고치지 않는다. active state에 제안을 기록하고 사용자가 결정한다.

## 6. Active state — 세션 간 handoff

`state/active/<task>.md`는 시간순 작업 일지가 아니라 현재 line of inquiry의 최신 snapshot이다.

핵심 필드는 다음과 같다.

```text
Outcome
Goal Connection
Current Hypothesis
Current Experiment
Latest Result
Interpretation
Decision
Next Experiment
Do Not
Verification and Evidence
```

Codex는 다음 시점에 파일을 갱신한다.

- 실험 정의가 확정될 때
- 구현이나 setup이 의미 있는 checkpoint에 도달할 때
- 실행 결과가 나올 때
- 해석, 판단, 다음 행동이 바뀔 때
- scope가 바뀔 때
- 세션을 멈추거나 handoff할 때

`계속 기록한다`는 모든 terminal command를 적는다는 뜻이 아니다. 다음 세션이 chat history 없이도 같은 판단 지점에서 재개할 수 있을 정도로 최신 상태를 보존한다는 뜻이다.

## 7. Experiment and Decision Ledger

`memory/experiments.md`는 장기적으로 다시 반복하면 안 되는 실패와 방향을 바꾼 판단을 보존한다.

각 entry는 다음 연결을 유지한다.

```text
Hypothesis
  -> Experiment
  -> Result
  -> Interpretation
  -> Decision
  -> Next action
```

숫자만 남기면 proxy metric의 작은 개선을 보고 같은 방향을 무한 최적화하기 쉽다. 따라서 결과가 무엇을 지지하고 무엇을 입증하지 못했는지, 접근을 채택·기각·중단했는지, 어떤 형태의 반복을 피해야 하는지를 함께 기록한다.

모든 run을 ledger에 넣지 않는다. 다음 중 하나에 해당할 때만 넣는다.

- 접근을 채택하거나 기각했다.
- 중요한 조건부 효과를 발견했다.
- 다음 방향이 바뀌었다.
- 형태만 바꾼 반복을 방지할 가치가 있다.

Raw log와 큰 결과물은 별도 위치에 두고 evidence path만 연결한다.

## 8. Drift review

일반 code review와 drift review는 목적이 다르다. Level 1 reviewer는 코드 스타일이나 architecture보다 실험 방향을 검사한다.

기본 cadence는 완료한 실험 다섯 회마다 한 번이다. 다음 signal이 있으면 더 일찍 실행한다.

- proxy metric이 실제 목표를 대신한다.
- 결과가 나쁘다는 이유로 scope나 complexity가 계속 늘어난다.
- 실패한 접근을 parameter나 이름만 바꿔 반복한다.
- 다음 실험을 `GOAL.md` criterion과 연결할 수 없다.
- stopping condition을 넘겼거나 GOAL 변경이 필요해 보인다.

검토 질문은 다음과 같다.

1. 현재 방향이 실제 장기 목표를 개선하는가?
2. proxy를 목표로 착각하고 있지 않은가?
3. 실패한 접근을 다른 형태로 반복하고 있지 않은가?
4. evidence 없이 scope나 complexity가 확장됐는가?
5. stopping condition이 지켜지고 있는가?
6. 판단을 바꿀 수 있는 가장 작은 다음 실험은 무엇인가?

가능하면 구현에 참여하지 않은 fresh read-only subagent가 검토한다. 공식 Codex subagent는 별도 thread에서 할당된 작업을 수행하고 메인 agent가 결과를 회수하는 방식이다. 저장소에서 자율적으로 상주하거나 모든 역할이 자동 순환하는 daemon이 아니다.

- https://learn.chatgpt.com/docs/agent-configuration/subagents

서브에이전트를 사용할 수 없으면 메인 agent가 구현 pass와 분리된 review pass로 수행하고 결과를 active state에 표시한다.

Active state의 `Drift Review`에는 완료한 총 실험 수, 마지막 검토 시점, 다음 검토 예정 시점, 관련 ledger entry, finding과 판단을 기록한다. 따라서 durable ledger에 남기지 않은 실험이 있어도 새 세션이 chat history 없이 cadence를 계산할 수 있다.

## 9. 실제 세션 흐름

```text
새 Codex 세션
  -> AGENTS.md 자동 적용
  -> GOAL.md 읽기
  -> 관련 active state 읽기
  -> 관련 experiment ledger 읽기
  -> 필요한 코드와 evidence만 조사
  -> 이번 가설과 최소 실험 정의
  -> 구현 또는 실행
  -> active state 갱신
  -> 필요한 경우 ledger append
  -> trigger 시 drift review
```

Root는 이 흐름을 조정한다. Coder는 구현을 직접 하는 main agent일 수도 있고, 메인 agent가 생성한 focused worker일 수도 있다. Coder는 persistent component가 아니다.

## 10. Level 2를 올리는 기준

다음 문제가 반복될 때만 architecture extension을 고려한다.

- 같은 behavior가 계속 잘못된 module에 배치된다.
- public boundary와 owner를 매 작업마다 다시 조사한다.
- cross-module internal access나 dependency cycle이 반복된다.
- 복잡한 subtree의 명령과 context를 지속적으로 놓친다.

Level 2가 추가할 수 있는 것은 다음과 같다.

- 현재 구조를 안내하는 `ARCHITECTURE.md`
- 반복되는 ownership confusion만 담는 domain memory
- 구조 문제를 조사하는 Steward
- 모듈형 구현 규칙을 가진 custom Coder
- placement와 boundary를 확인하는 Architecture Reviewer
- 실제 local constraint가 있는 subtree의 local `AGENTS.md`

Level 2에서도 root `AGENTS.md`에 모든 역할의 상세 실행 규칙을 넣지 않는다. 공통 routing만 병합하고 Coder, Reviewer, Steward의 상세 지침은 `.codex/agents/*.toml`에 둔다.

## 11. 적용

Level 1 설치:

```bash
cp -R /path/to/codex-repository-framework/level-1-continuity/. /path/to/target-project/
```

그 다음 사용자가 `GOAL.md`를 작성하고 첫 active state를 만든다.

```bash
cd /path/to/target-project
cp state/active/_template.md state/active/<task>.md
```

Level 2는 반복 문제가 확인된 뒤 extension README에 따라 overlay를 병합한다.

## 12. 핵심 판단

이 구조의 핵심은 정보를 많이 보존하는 것이 아니다.

- `GOAL.md`는 바뀌면 안 되는 기준을 보존한다.
- `state/active`는 지금 어디까지 왔는지를 보존한다.
- `memory/experiments.md`는 다시 하지 말아야 할 것과 판단 이유를 보존한다.
- drift review는 이 셋의 연결이 끊겼는지 독립적으로 확인한다.

Architecture governance는 이 continuity loop가 해결하지 못하는 실제 구조 문제가 관측된 뒤에만 추가한다.
