# Codex Repository Framework

이 폴더는 다른 프로젝트의 루트에 그대로 복사하기 위한 최소 프레임입니다.

핵심 원칙은 다음과 같습니다.

> Context should be discovered globally, but loaded locally.

Codex는 `AGENTS.md`에서 공통 판단 순서를 익히고, `ARCHITECTURE.md`와 `scripts/memory-map`으로 필요한 지식을 찾은 뒤, 현재 작업과 관련된 memory만 읽습니다.

## 구성

```text
.
├── AGENTS.md
├── ARCHITECTURE.md
├── agents/
│   ├── coder.md
│   ├── reviewer.md
│   └── steward.md
├── memory/
│   ├── direction.md
│   ├── domains/
│   │   └── _template.md
│   ├── work/
│   │   └── _template.md
│   └── decisions/
│       └── _template.md
└── scripts/
    ├── check
    └── memory-map
```

## 적용하기

이 디렉터리의 **내용**을 대상 프로젝트 루트에 복사합니다.

```bash
cp -R /path/to/codex-repository-framework/. /path/to/target-project/
cd /path/to/target-project
./scripts/memory-map
./scripts/check
```

기존 `AGENTS.md`, `ARCHITECTURE.md`, `memory/`, `scripts/`가 있다면 덮어쓰기 전에 내용을 병합해야 합니다.

## 프로젝트별 초기화

### 1. 현재 구조 기록

`ARCHITECTURE.md`에는 이상적인 미래 구조가 아니라 현재 구조를 기록합니다. 각 주요 경로가 무엇을 소유하는지와 legacy/transitional 영역을 명시합니다.

### 2. 방향 정리

`memory/direction.md`의 공통 원칙을 유지하면서 프로젝트 특유의 선호와 금지 패턴을 추가합니다.

### 3. 필요한 도메인만 생성

ownership 혼동이 있거나 독립적인 의미 경계가 있는 영역부터 `memory/domains/_template.md`를 복사해 작성합니다. 모든 폴더나 기능에 문서를 만들 필요는 없습니다.

### 4. 검증 연결

`scripts/check`의 표시된 영역에 프로젝트의 lint, test, typecheck, build 명령을 연결합니다. 기본 상태에서는 프레임 자체 점검만 수행합니다.

## Memory 운영 규칙

- `domains/`: 도메인의 ownership, boundary, 현재 방향이 필요할 때만 추가합니다.
- `work/`: 한 Codex 작업 컨텍스트를 넘어가는 활성 작업에만 사용하고, 완료 후 정리합니다.
- `decisions/`: 코드만으로 이유를 복원하기 어렵고 반복해서 뒤집힐 수 있는 결정만 기록합니다.
- `_template.md`: 작성 형식이며 프로젝트 지식으로 간주하지 않습니다.

generated dashboard, health registry, 복잡한 schema, memory build pipeline은 반복되는 실제 문제가 생기기 전에는 추가하지 않습니다.
