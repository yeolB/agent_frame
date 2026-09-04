# Codex Repository Framework

이 폴더는 다른 프로젝트의 루트에 복사하기 위한 최소 Codex 프레임입니다.

핵심 원칙은 다음과 같습니다.

> Context should be discovered globally, but loaded locally.

루트 `AGENTS.md`는 모든 작업에 적용되는 의사결정 커널이자 최초 context 전파 노드입니다. 역할별 실행은 공식 프로젝트 커스텀 에이전트인 `.codex/agents/*.toml`이 담당합니다. 현재 작업 상태는 `state/`, 오래 유지할 지식은 `memory/`에 분리합니다.

## 구성

```text
.
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
│   │   └── _template.md
│   └── decisions/
│       └── _template.md
└── scripts/
    ├── check
    └── context-map
```

## 적용하기

이 디렉터리의 **내용**을 대상 프로젝트 루트에 복사합니다. `/.`을 포함해야 숨김 폴더인 `.codex/`도 함께 복사됩니다.

```bash
cp -R /path/to/codex-repository-framework/. /path/to/target-project/
cd /path/to/target-project
./scripts/context-map
./scripts/check
```

기존 `AGENTS.md`, `.codex/`, `ARCHITECTURE.md`, `state/`, `memory/`, `scripts/`가 있다면 덮어쓰기 전에 병합합니다.

## 실행 모델

하나의 사용자 작업은 메인 세션의 Root 에이전트가 조정합니다. Root는 필요할 때 별도 에이전트 스레드로 `steward`, `coder`, `reviewer`를 생성하고, 각 결과를 기다린 뒤 통합합니다.

커스텀 에이전트는 저장소 안에서 계속 실행되는 daemon이 아니며 세션 시작 시 모두 자동으로 실행되지도 않습니다. 사용자 요청이나 적용 중인 `AGENTS.md`가 위임을 요구할 때 생성되고, 할당된 작업을 독립적인 컨텍스트에서 수행한 뒤 결과를 Root에 반환합니다.

기본 순서는 다음과 같습니다.

```text
일반 구현
Root → Coder → Reviewer → Root 통합

새 프로젝트 또는 주요 subsystem
Root → Steward 설계 제안 → Coder 구현 → Reviewer 검토 → Root 통합
```

서로 독립적인 읽기·탐색·분석은 병렬 실행할 수 있습니다. 같은 파일이나 경계를 수정하는 쓰기 에이전트는 충돌을 피하기 위해 순차 실행합니다.

Codex의 하위 에이전트와 프로젝트 커스텀 에이전트 동작은 [공식 OpenAI 문서](https://learn.chatgpt.com/ko-KR/docs/agent-configuration/subagents)를 참고하세요.

## Root의 책임

`AGENTS.md`는 단순한 역할 목록이 아닙니다. 다음을 소유합니다.

- 모든 역할이 공유하는 의사결정 순서
- ownership, locality, modularity, dependency 원칙
- 필요한 context를 찾는 순서
- 역할과 실행 순서 선택
- 하위 에이전트에 전달할 task packet
- 결과 통합과 완료 판단

Root는 하위 에이전트에 프로젝트 전체 context를 복사하지 않습니다. 원래 요청, 관찰 가능한 결과, 검증해야 할 ownership 가설, 관련 context 경로, 제약, 비목표, 상태 파일, 검증 기준, 반환 형식을 전달합니다.

## 커스텀 에이전트

프로젝트 범위의 커스텀 에이전트는 `.codex/agents/*.toml`로 정의합니다.

- `coder`: 구현, 코드 생성, active-state 갱신, 검증
- `reviewer`: 구현자의 해석을 독립적으로 재검토하는 read-only 역할
- `steward`: 초기 모듈 구조 제안, ownership 탐색, 장기 구조 관리

프레임은 특정 모델이나 reasoning effort를 고정하지 않습니다. 에이전트는 적용하는 환경의 설정을 상속하므로 프로젝트별 필요가 확인됐을 때만 TOML에 모델 설정을 추가합니다.

## 모듈형 초기 설계

새 프로젝트나 주요 subsystem은 파일부터 생성하지 않습니다.

1. Steward가 핵심 행동과 owner 후보를 식별합니다.
2. 최소한의 cohesive module과 공개 경계를 제안합니다.
3. 허용할 dependency direction과 외부 adapter 경계를 정합니다.
4. 제안은 구현 전까지 `state/active/<task>.md`에 둡니다.
5. Coder가 검증된 경계에 맞춰 구현합니다.
6. 실제 구조가 만들어진 후 `ARCHITECTURE.md`를 현재 현실에 맞게 작성합니다.
7. Reviewer가 cohesion, 공개 경계, dependency cycle, 과도한 추상화를 검사합니다.

모듈형 설계는 module 수를 늘리는 것이 아닙니다. 현재 행동을 명확히 소유하는 최소 module을 만들고, 독립 배포나 운영 격리가 실제 요구가 아니라면 in-process boundary를 우선합니다.

## Active state

`state/active/<task>.md`는 중요한 진행 작업의 최신 checkpoint입니다. 작업 일지나 backlog가 아닙니다.

다음 작업은 시작할 때 active-state 파일을 만듭니다.

- 여러 단계로 진행되는 작업
- 여러 domain 또는 module을 건드리는 작업
- migration이나 큰 refactoring
- 재조사 비용이 큰 작업
- 한 worker context를 넘길 가능성이 있는 작업

Coder는 milestone, 범위·접근 변경, 중요한 발견, 검증 상태 변경, 중단·handoff 전에 갱신합니다. 완료 후 지속할 상태가 없으면 삭제하고, 장기적으로 필요한 지식만 `memory/`로 옮깁니다. 시간순 기록은 Git history에 맡깁니다.

## Durable memory

- `direction.md`: 구현 선택에 사용하는 장기 engineering direction
- `domains/`: 코드만으로 불명확한 ownership과 boundary
- `decisions/`: 반복해서 뒤집힐 위험이 있는 결정의 이유

모든 폴더나 기능에 domain 문서를 만들지 않습니다. ownership 혼동, boundary 위반, 반복 재조사가 실제로 발생하는 영역부터 추가합니다.

## 프로젝트별 초기화

1. `ARCHITECTURE.md`에 이상적인 미래가 아니라 현재 구조를 기록합니다.
2. `memory/direction.md`에 프로젝트 고유의 장기 판단 기준을 추가합니다.
3. 필요한 domain부터 `memory/domains/_template.md`를 복사해 작성합니다.
4. `scripts/check`에 실제 lint, typecheck, test, build 명령을 연결합니다.
5. 새 코드베이스라면 Root가 Steward → Coder → Reviewer 순서로 초기 module 구조를 구축하게 합니다.

generated dashboard, health registry, 복잡한 metadata schema, 자동 memory build pipeline은 반복되는 실제 문제가 생기기 전에는 추가하지 않습니다.
