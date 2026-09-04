# Codex Experimental Continuity Framework

이 번들은 긴 실험 작업을 여러 Codex 세션으로 나눠도 장기 목표, 현재 가설, 평가 기준, 이미 배운 실패가 끊기지 않게 하기 위한 프레임입니다.

기본값은 Level 1입니다. Architecture governance는 실제 구조 문제가 반복해서 관측될 때만 Level 2로 추가합니다.

## Level 1 — Continuity

대상 프로젝트 루트에 `level-1-continuity/`의 **내용**을 복사합니다.

```bash
cp -R /path/to/codex-repository-framework/level-1-continuity/. /path/to/target-project/
```

설치되는 핵심 파일군은 네 개뿐입니다.

```text
AGENTS.md
GOAL.md
state/active/<task>.md
memory/experiments.md
```

적용 직후 사용자가 `GOAL.md`를 작성합니다. Codex는 이를 임의로 바꾸지 않습니다. 새 세션의 context 순서는 다음과 같습니다.

```text
AGENTS.md
  -> GOAL.md
  -> state/active/<task>.md
  -> memory/experiments.md의 관련 항목
  -> 필요한 코드와 결과
```

`state/active/_template.md`를 복사해 현재 실험 파일을 만듭니다.

```bash
cp state/active/_template.md state/active/strategy-search.md
```

Codex는 실험 정의, 구현 checkpoint, 결과 발생, 해석·판단 변경, 중단·handoff 때 active state를 갱신합니다. 모든 행동을 기록하는 일지는 만들지 않습니다.

`memory/experiments.md`에는 미래에 반복을 막거나 방향을 바꾸는 실험만 `가설 -> 실험 -> 결과 -> 해석 -> 판단 -> 다음 행동` 형태로 남깁니다.

## Drift review

기본 cadence는 완료한 실험 다섯 회마다 한 번입니다. Active state가 완료 횟수와 다음 검토 시점을 보존합니다. 목표와 연결되지 않는 실험, proxy metric의 목표화, 실패한 접근의 변형 반복, 근거 없는 scope·complexity 확대가 보이면 더 일찍 실행합니다.

서브에이전트를 사용할 수 있으면 구현에 참여하지 않은 새 read-only agent가 검토합니다. 이는 상주 프로세스나 자동 daemon이 아니라 메인 세션이 필요한 시점에 생성하고 결과를 회수하는 작업입니다. 서브에이전트가 없으면 메인 agent가 별도 review pass로 같은 질문을 검사합니다.

## Level 2 — Architecture

다음 문제가 실제로 반복될 때만 [`level-2-architecture/`](./level-2-architecture/)를 검토합니다.

- Codex가 behavior를 계속 잘못된 위치에 구현한다.
- module ownership이나 public boundary를 반복해서 재조사한다.
- 복잡한 subtree에서 필요한 코드와 지침을 지속적으로 찾지 못한다.
- dependency direction이나 local operational constraint가 반복해서 깨진다.

Level 2는 `ARCHITECTURE.md`, ownership/domain memory, Steward, custom coder/reviewer, local `AGENTS.md`를 선택적으로 추가합니다. Level 1에서 이런 문제를 미리 가정하지 않습니다.
