# Codex-only / AI-only Repository Framework v2.2

새 프로젝트를 모듈형으로 시작하거나 기존 프로젝트에 점진적으로 도입하기 위한 최소 AI 개발 프레임

## 1. 목적

이 프레임은 특정 애플리케이션의 아키텍처를 정의하지 않는다. 프로젝트마다 교체될 수 있는 Codex worker가 공통 판단 기준을 공유하고, 현재 작업에 필요한 프로젝트 지식만 찾아서 일관되게 작업하도록 만드는 저장소 구조다.

핵심 원칙은 다음과 같다.

> Context should be discovered globally, but loaded locally.

어떤 정보가 존재하는지는 빠르게 발견할 수 있어야 하지만 실제 context에는 현재 작업에 필요한 정보만 로드한다.

## 2. 실행 모델

하나의 사용자 작업은 메인 세션의 Root 에이전트가 조정한다. Root는 요청을 해석하고 공통 의사결정 구조를 적용한 뒤 필요한 역할을 별도 에이전트 스레드로 생성한다.

```text
일반 구현
Root → Coder → Reviewer → Root 통합

새 프로젝트 또는 주요 subsystem
Root → Steward 설계 제안 → Coder 구현 → Reviewer 검토 → Root 통합
```

각 하위 에이전트는 자기 컨텍스트에서 할당된 작업을 수행하고 결과를 Root에 반환한다. 에이전트가 저장소 안에서 daemon처럼 상주하거나 모든 역할이 세션 시작 시 자동으로 순환하는 구조는 아니다. Root가 생성, 후속 지시, 대기, 결과 통합을 조정한다.

독립적인 읽기·탐색·분석은 병렬화할 수 있다. 동일 파일이나 동일 경계를 수정하는 쓰기 작업은 충돌을 피하기 위해 순차 실행한다.

## 3. 책임 계층

```text
AGENTS.md
  공통 의사결정과 최초 context 전파
        ↓
.codex/agents/*.toml
  역할별 실행 절차
        ↓
ARCHITECTURE.md / state / memory / code
  선택적으로 로드하는 프로젝트 context
```

- `AGENTS.md`: repository-wide policy plane
- `.codex/agents/*.toml`: role-specific execution plane
- `ARCHITECTURE.md`, `state/`, `memory/`: context plane
- 실제 코드와 테스트: 최종 사실의 원천

## 4. Context loading hierarchy

### Level 0 — Always load

`AGENTS.md`에서 공통 의사결정, 설계 원칙, context routing, 역할 선택 규칙을 읽는다.

### Level 1 — Orient

`ARCHITECTURE.md` 또는 `./scripts/context-map`으로 owner 후보와 관련 context 위치를 찾는다.

### Level 2 — Load local meaning and state

현재 작업에 관련된 다음 파일만 읽는다.

- `state/active/<task>.md`
- `memory/domains/<domain>.md`
- 적용되는 하위 `AGENTS.md`

### Level 3 — Deep context when needed

관련 코드, 테스트, decision 문서, 인접 domain을 필요할 때만 추가로 읽는다.

## 5. 권장 저장소 구조

```text
repo/
├── AGENTS.md
├── ARCHITECTURE.md
├── .codex/
│   └── agents/
│       ├── coder.toml
│       ├── reviewer.toml
│       └── steward.toml
├── state/
│   ├── README.md
│   ├── _task-template.md
│   └── active/
├── memory/
│   ├── direction.md
│   ├── domains/
│   │   ├── _README.md
│   │   ├── _template.md
│   │   └── _index-template.md
│   └── decisions/
│       └── _template.md
├── scripts/
│   ├── check
│   └── context-map
├── templates/
│   ├── local-AGENTS.md
│   └── local-ARCHITECTURE.md
└── <actual project code>
```

이 구조는 의도적으로 작다. 실제 반복 문제가 없는 dashboard, registry, 복잡한 schema, 자동 memory build pipeline은 만들지 않는다.

## 6. AGENTS.md — 공통 의사결정과 최초 전파 노드

루트 `AGENTS.md`는 단순한 agent 목록이 아니다. 모든 역할이 공유하는 다음 책임을 가진다.

1. 사용자가 요구한 관찰 가능한 결과를 확인한다.
2. 현재 구조와 owner 후보를 찾는다.
3. 이를 검증하는 데 필요한 최소 context를 선택한다.
4. 현재 사실과 장기 방향을 구분한다.
5. 최소한의 일관된 작업과 명시적 비목표를 정한다.
6. 적합한 역할과 실행 순서를 선택한다.
7. 위험에 비례해 결과를 검증한다.
8. 미래 작업에 필요한 상태와 지식만 남긴다.

또한 ownership, locality, cohesive module, 명시적인 public boundary, 단방향 dependency 같은 repository-wide 설계 원칙을 제공한다.

## 7. Task packet — Root가 전달하는 최소 작업 context

Root는 하위 에이전트에 전체 프로젝트 context를 복사하지 않는다. 다음 task packet을 전달한다.

```text
Task
  사용자의 원래 요청

Outcome
  완료를 판단할 수 있는 결과

Ownership hypothesis
  담당 agent가 검증해야 할 owner 후보

Context pointers
  관련 architecture, state, domain, decision 경로

Constraints / Non-goals
  지켜야 할 경계와 변경하지 않을 영역

State path
  생성하거나 갱신할 active checkpoint

Verification
  필요한 검사와 완료 기준

Return
  Root에 반환할 결과 형식
```

Root가 구현을 미리 확정하지 않고, 책임 agent가 로컬 현실을 확인하도록 한다.

## 8. 공식 프로젝트 커스텀 에이전트

역할은 `.codex/agents/*.toml`로 정의한다. 각 파일에는 `name`, `description`, `developer_instructions`가 필요하다.

프레임은 특정 모델이나 reasoning effort를 고정하지 않는다. 적용 환경을 상속하고, 프로젝트에서 필요성이 확인됐을 때만 추가한다.

자세한 형식은 OpenAI 공식 문서를 따른다.

- https://learn.chatgpt.com/ko-KR/docs/agent-configuration/subagents

## 9. Coder

Coder는 구현, code generation, refactoring, active-state 갱신, 검증을 담당하는 ephemeral worker다.

Coder는 작업 전에 owner, layer, 최소 context, 최소 변경, 비목표를 확인한다. 기존 코드는 자동으로 precedent가 아니며 문서화된 legacy와 local exception을 확장하지 않는다.

중요 작업에서는 `state/active/<task>.md`를 생성하고 milestone, 범위 변경, 중요한 발견, 검증 상태 변경, 중단과 handoff 전에 최신 상태로 갱신한다.

## 10. 새 코드의 모듈형 설계

새 프로젝트, 주요 subsystem, 비중 있는 module을 생성할 때 구현 파일부터 만들지 않는다.

1. 핵심 behavior와 각 behavior의 owner를 식별한다.
2. 우연한 기술적 유사성이 아니라 cohesive responsibility로 코드를 묶는다.
3. module의 public interface와 private internal model을 구분한다.
4. 허용 dependency direction을 정하고 cycle을 피한다.
5. transport, framework, storage, provider detail을 명시적인 edge에 둔다.
6. 현재 behavior를 소유하는 최소한의 module만 만든다.
7. 미래 소비자를 가정한 abstraction과 shared dumping ground를 만들지 않는다.

독립 배포나 운영 격리가 실제 요구가 아니라면 in-process module boundary를 우선한다. 모듈형 설계는 microservice화를 의미하지 않는다.

구현 전 제안은 active state에 기록하고, 실제 구조가 만들어진 뒤에만 `ARCHITECTURE.md`를 현재 현실에 맞게 갱신한다.

## 11. Reviewer

Reviewer는 Coder의 해석을 그대로 받아들이지 않는다. 원래 요청에서 owner, 올바른 layer, 최소 변경 면적, relevant direction을 독립적으로 재구성한 뒤 구현과 비교한다.

검토 항목은 다음과 같다.

- behavior correctness
- ownership과 placement
- module cohesion과 public boundary
- dependency direction과 cycle
- 불필요한 dependency와 abstraction
- 요구사항에 비해 과도한 change surface
- legacy exception을 precedent로 확장했는지
- active-state 정확성
- 위험에 적합한 verification

Reviewer는 기본적으로 read-only다.

## 12. Steward

Steward는 미래 agent가 물려받을 repository 자체를 개선한다.

새 프로젝트나 주요 subsystem에서는 핵심 behavior, owner 후보, public boundary, 외부 edge를 조사하고 최소 module 구조를 제안한다. 기존 프로젝트에서는 현재 현실을 먼저 기록한 뒤 ownership confusion, 잘못된 behavior placement, 깊은 dependency chain, locality 저하, memory drift를 찾는다.

문서나 governance를 늘리기 전에 code placement, naming, boundary, routing을 개선할 수 있는지 먼저 판단한다.

## 13. state/ — 현재 진행 상태

`state/`는 자주 바뀌는 operational state를 보관한다. durable knowledge를 담는 `memory/`와 분리한다.

다음 작업에는 `state/active/<task>.md`를 만든다.

- 여러 단계로 진행되는 작업
- 여러 domain 또는 module을 건드리는 작업
- migration이나 큰 refactoring
- 재조사 비용이 큰 작업
- 한 worker context를 넘길 가능성이 있는 작업

파일은 chronological diary가 아니라 최신 checkpoint다.

```text
Outcome
Scope
Working Plan
Current
Next
Decisions
Findings
Do Not
Verification
```

완료 후 handoff할 상태가 없으면 active 파일을 삭제한다. 시간순 이력은 Git이 보존한다.

## 14. ARCHITECTURE.md — 현재 구조의 routing map

Architecture 문서는 현재 존재하는 repository와 module 구조를 설명한다.

- 주요 path와 owner
- cohesive module과 public entry point
- dependency direction
- module 간 public interaction
- internal model이 넘어가면 안 되는 boundary
- transitional 또는 legacy area

아직 구현되지 않은 목표 구조는 Architecture의 현재 사실처럼 기록하지 않는다.

작은 프로젝트는 루트 Architecture 하나로 시작한다. 특정 subtree의 내부 구조 때문에 루트 문서가 간결한 routing map 역할을 할 수 없을 때만 detail을 가장 가까운 local Architecture로 승격한다.

```text
ARCHITECTURE.md
  └─ services/payments/ARCHITECTURE.md
       └─ memory/domains/payments/index.md
            ├─ boundaries.md
            └─ flows/refunds.md
```

루트 문서는 subtree의 owner와 local-map 링크만 유지한다. Local Architecture는 해당 subtree의 현재 module map, public entry point, dependency direction, transitional area만 설명하고 루트 내용을 복사하지 않는다.

## 15. memory/direction.md — 장기 판단 기준

Direction은 특정 기능 설명이 아니라 두 구현이 모두 동작할 때 선택할 기준이다.

- locality over abstraction
- ownership over convenience
- cohesive module with explicit boundary
- visible dependency direction
- concrete implementation over speculative framework
- small change over broad migration

## 16. memory/domains/ — 필요한 ownership만 기록

Domain memory는 모든 디렉터리의 설명서가 아니다. 코드만으로 ownership이나 boundary가 불명확하고 반복 오류 비용이 있을 때만 만든다.

좋은 domain 문서는 다음에 답한다.

- 무엇을 소유하는가?
- 무엇을 소유하지 않는가?
- 다른 module은 어떻게 접근할 수 있는가?
- 어떤 internal access가 금지되는가?
- 어떤 패턴이 preferred, tolerated, local exception인가?
- 현재 상태에서 어느 방향으로 이동하는가?

### Domain memory lifecycle

Domain memory는 다음 조건 중 하나가 있을 때만 만든다.

- ownership이 코드와 Architecture만으로 명확하지 않다.
- behavior가 반복해서 잘못된 module에 배치된다.
- 다른 module이 internal boundary를 위반하기 쉽다.
- 같은 invariant 또는 exception이 반복해서 재발견된다.
- preferred pattern과 tolerated legacy를 구분해야 한다.

Source directory, package, data type, CRUD 기능은 자동으로 domain이 아니다.

처음에는 `memory/domains/<domain>.md` 한 파일로 시작한다. 서로 다른 작업이 관련 없는 detail을 함께 읽어야 할 때만 다음과 같이 승격한다.

```text
memory/domains/payments/
├── index.md
├── boundaries.md
└── flows/
    └── refunds.md
```

`index.md`는 ownership과 public boundary를 짧게 유지하고 세부 context로 routing한다. 파일 길이 자체는 분할 근거가 아니며, 독립적인 작업에 독립적인 context가 필요한지가 기준이다.

같은 owner를 설명하거나 의미 있는 독립 boundary가 없거나 항상 함께 읽는 domain은 합친다. Code와 Architecture만으로 내용이 충분히 명확해지거나 더 이상 판단을 바꾸지 않는 domain memory는 제거한다. 필요한 결정 이유만 decision 문서로 옮기고 Git history에 이전 내용을 맡긴다.

Domain memory가 두 번째 architecture wiki가 되거나 구현 detail과 계속 동기화해야 한다면 범위를 줄이거나 제거한다.

## 17. memory/decisions/ — 필요한 이유만 보존

Decision 문서는 코드만으로 이유를 복구하기 어렵고 미래 agent가 쉽게 뒤집어 반복 문제를 만들 수 있는 결정에만 사용한다. 일반 구현 세부사항과 작업 진행은 기록하지 않는다.

## 18. 하위 AGENTS.md — 필요한 local delta만 적용

하위 `AGENTS.md` 또는 `AGENTS.override.md`는 subtree에 별도 command, operational constraint, review rule, 반복되는 local mistake가 있을 때만 만든다.

하위 파일은 루트 `AGENTS.md`를 복사하지 않는다. Scope, local constraint, local verification, 명시적 override와 이유만 기록한다. Domain 설명이나 architecture detail은 넣지 않고 해당 local Architecture 또는 domain memory로 연결한다.

Codex는 프로젝트 루트에서 현재 working directory까지의 지침을 결합하고 더 가까운 파일을 나중에 적용한다. Root에서 시작한 agent는 변경 대상 경로의 local instruction을 명시적으로 확인해야 한다. Local template은 `templates/local-AGENTS.md`에 둔다.

- https://learn.chatgpt.com/docs/agent-configuration/agents-md

## 19. context-map — 읽기 전에 발견하기

`./scripts/context-map`은 다음을 deterministic하게 보여준다.

- `memory/**/*.md`의 경로와 첫 H1
- `state/active/*.md`의 경로와 첫 H1

이름이 `_`로 시작하는 framework guidance와 template은 결과에서 제외한다. AI 요약이나 중요도 판단은 하지 않는다. 무엇이 있는지 확인한 뒤 필요한 파일만 선택해서 읽게 한다.

## 20. 일반 작업 시나리오

```text
1. Root가 AGENTS.md의 decision kernel 적용
2. ARCHITECTURE.md / context-map으로 owner와 context 후보 발견
3. Root가 task packet 구성
4. Coder 생성
5. Coder가 ownership과 boundary 검증
6. 필요한 active state 생성 또는 갱신
7. 최소 변경 구현 및 check 실행
8. Reviewer가 독립적으로 재검토
9. Root가 결과 통합
10. active state 정리 및 필요한 durable memory만 반영
```

## 21. 새 프로젝트 도입

1. 프레임 내용을 프로젝트 루트에 복사한다.
2. Root가 Steward에게 최소 module 및 ownership 제안을 요청한다.
3. 제안을 active state에 기록한다.
4. Coder가 최소 skeleton과 첫 behavior를 구현한다.
5. 실제 구조를 `ARCHITECTURE.md`에 기록한다.
6. Reviewer가 boundary와 dependency shape을 검토한다.
7. 실제 ownership 혼동이 생길 때만 domain memory를 추가한다.

## 22. 기존 프로젝트 도입

1. 재설계 전에 현재 path, entry point, module, dependency를 조사한다.
2. `ARCHITECTURE.md`에 현재 현실과 transitional area를 기록한다.
3. 반복적으로 혼동되는 owner부터 domain memory를 만든다.
4. 현재 흔하지만 확장하면 안 되는 패턴을 tolerated 또는 local exception으로 표시한다.
5. 대규모 migration 대신 이후 작업에서 작은 방향성 개선을 누적한다.
6. 루트 routing이 부족해질 때만 local Architecture, domain index, 하위 AGENTS를 추가한다.

## 23. 만들지 않는 것

초기에는 다음을 만들지 않는다.

- generated index 또는 dashboard
- migration dashboard
- health registry
- 복잡한 frontmatter/schema
- 자동 memory-build pipeline
- 모든 기능에 대한 domain 문서
- 미래 확장을 위한 추상 module

반복되는 실제 비용이 확인될 때만 추가한다.

## 24. 최종 원칙

1. Root는 공통 의사결정과 최초 context 전파를 소유한다.
2. 역할별 실행 지침은 공식 custom-agent TOML에 둔다.
3. Ownership precedes implementation.
4. Context is discovered globally but loaded locally.
5. 새 코드는 최소한의 cohesive module과 명시적 boundary로 시작한다.
6. Active state와 durable memory를 분리한다.
7. Coder는 중요한 작업의 최신 checkpoint를 유지한다.
8. Reviewer는 문제를 독립적으로 재구성한다.
9. Steward는 문서가 아니라 미래 repository를 개선한다.
10. Governance는 해결하는 문제보다 복잡해지면 안 된다.
11. Domain memory와 local instructions는 반복 판단 비용을 줄이는 동안만 유지한다.
12. 복잡성은 필요가 증명될 때 root map에서 local map으로 한 단계씩 승격한다.
