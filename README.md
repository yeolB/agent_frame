# Codex-only Repository Framework

Codex가 프로젝트 전체 지식을 매번 읽지 않고도, 현재 작업에 필요한 맥락을 찾아서 작업하도록 만드는 재사용 가능한 저장소 프레임입니다.

설계 배경과 원칙은 [`codex_ai_only_repository_framework_guide_v2-1.docx`](./codex_ai_only_repository_framework_guide_v2-1.docx)에 정리되어 있고, 실제 프로젝트에 복사할 파일은 [`codex-repository-framework/`](./codex-repository-framework/)에 있습니다.

## 빠른 적용

새 프로젝트 또는 기존 프로젝트의 루트에서 다음처럼 프레임 내용을 복사합니다.

```bash
cp -R /path/to/agent_frame/codex-repository-framework/. .
```

복사 후에는 다음 항목만 프로젝트 현실에 맞게 작성합니다.

1. `ARCHITECTURE.md`에 현재 코드 구조와 ownership을 기록합니다.
2. `memory/direction.md`에 프로젝트 고유의 장기 방향을 추가합니다.
3. 필요한 도메인부터 `memory/domains/_template.md`를 복사해 작성합니다.
4. `scripts/check`에 프로젝트의 실제 검증 명령을 연결합니다.

자세한 적용 방법은 [`codex-repository-framework/README.md`](./codex-repository-framework/README.md)를 참고하세요.
