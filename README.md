# Codex Experimental Continuity Framework

긴 실험 작업을 여러 세션으로 나눠도 Codex가 장기 목표, 평가 기준, 현재 가설, 이미 배운 실패를 잊지 않고 이어가게 하는 재사용 프레임입니다.

실제 프로젝트에 복사할 파일과 적용 설명은 [`codex-repository-framework/`](./codex-repository-framework/)에 있습니다. 기본 설치는 네 파일군으로 구성된 **Level 1 — Continuity**이며, architecture governance는 관측된 구조 문제가 생겼을 때만 **Level 2**로 추가합니다.

## 빠른 적용

새 프로젝트 또는 기존 프로젝트의 루트에서 Level 1의 내용만 복사합니다.

```bash
cp -R /path/to/agent_frame/codex-repository-framework/level-1-continuity/. .
```

복사 후 사용자가 `GOAL.md`에 장기 목적, 성공 기준, 금지할 proxy 최적화, 중단 조건, 핵심 가설을 작성합니다. Codex는 명시적 사용자 요청 없이 이 파일을 변경하지 않습니다.

자세한 적용 방법은 [`codex-repository-framework/README.md`](./codex-repository-framework/README.md)를 참고하세요.

현재 설계 문서는 [`docs/codex_experimental_continuity_framework_guide_v3-0.md`](./docs/codex_experimental_continuity_framework_guide_v3-0.md)입니다. v2.1과 v2.2는 범용 architecture framework로 확장됐던 이전 설계 기록으로 유지합니다.
