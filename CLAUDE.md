# MCP 기반 사실 확인 챗봇 에이전트

## 프로젝트 개요

MCP(Model Context Protocol)를 활용하여 다양한 주제에 대해 **사실 기반** 대화를 제공하는 독립형 챗봇 에이전트입니다.

## 핵심 기능

1. **사실 기반 대화**: 웹 검색을 통해 검증된 정보 제공
2. **Multi-turn 대화**: 대화 컨텍스트를 유지하며 연속적인 대화 지원
3. **REST API**: 독립적으로 작동하는 Chat API 제공
4. **MCP 통합**: DuckDuckGo/Brave Search, Fetch MCP 서버 연동

## 기술 스택

- **언어**: Python 3.11+
- **웹 프레임워크**: FastAPI
- **MCP 클라이언트**: mcp 라이브러리
- **LLM**: Claude API (anthropic)
- **세션 관리**: 인메모리

## 프로젝트 구조

```
mcp_for_chat/
├── CLAUDE.md              # 프로젝트 문서 (개발용)
├── README.md              # 사용 가이드
├── requirements.txt       # 의존성
├── .env.example           # 환경변수 템플릿
├── src/
│   ├── main.py            # FastAPI 앱 진입점, MCP 초기화
│   ├── config.py          # 설정 관리
│   ├── api/
│   │   ├── routes.py      # API 라우트 (/chat, /sessions, /health)
│   │   └── models.py      # Pydantic 요청/응답 모델
│   ├── agent/
│   │   ├── chatbot.py     # 챗봇 에이전트 (Claude + MCP 도구 호출)
│   │   └── session.py     # 세션/컨텍스트 관리
│   └── mcp/
│       ├── client.py      # MCP 클라이언트 (stdio 통신)
│       └── tools.py       # MCP 서버 설정
└── tests/
```

## API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| POST | `/chat` | 메시지 전송 및 응답 |
| GET | `/sessions/{session_id}` | 세션 정보 조회 |
| DELETE | `/sessions/{session_id}` | 세션 삭제 |
| GET | `/health` | 헬스체크 (사용 가능한 도구 수 포함) |

## MCP 서버

| 서버 | 용도 | 환경변수 |
|------|------|----------|
| DuckDuckGo | 웹 검색 (기본값) | `SEARCH_PROVIDER=duckduckgo` |
| Brave Search | 웹 검색 (프로덕션) | `SEARCH_PROVIDER=brave`, `BRAVE_API_KEY` |
| Fetch | 웹페이지 내용 가져오기 | 항상 활성화 |

## 구현 현황

### Phase 1: 기본 구조 (MVP) ✅
- [x] 프로젝트 초기 설정
- [x] FastAPI 기본 구조
- [x] 챗봇 에이전트 (Claude API)
- [x] 세션 관리 (인메모리)
- [x] 기본 API 엔드포인트

### Phase 2: MCP 통합 ✅
- [x] MCP 클라이언트 구현
- [x] DuckDuckGo/Brave Search 연동
- [x] Fetch MCP 연동
- [x] 도구 호출 루프 구현
- [x] 소스 URL 수집

### Phase 3: 고도화 (TODO)
- [ ] 스트리밍 응답 지원
- [ ] 에러 처리 강화
- [ ] 테스트 코드 작성
- [ ] Redis 세션 저장소

## 환경 변수

```bash
ANTHROPIC_API_KEY=your-api-key      # 필수
SEARCH_PROVIDER=duckduckgo          # duckduckgo (기본) 또는 brave
BRAVE_API_KEY=your-brave-api-key    # SEARCH_PROVIDER=brave 일 때 필요
LOG_LEVEL=INFO
SESSION_TIMEOUT=3600
```

## 개발 명령어

```bash
# 의존성 설치
pip install -r requirements.txt

# uv 설치 (MCP 서버 실행에 필요)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 개발 서버 실행
uvicorn src.main:app --reload --port 8000

# API 문서
# http://localhost:8000/docs
```
