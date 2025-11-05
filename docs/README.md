# True North Audio - Documentation Index

## 📚 Documentation Overview

Complete documentation for the True North Audio AI music generation platform.

---

## 🚀 Getting Started

### New User? Start Here
1. **[README.md](../README.md)** - Project overview and quick start
2. **[MACHINE-SETUP-CHECKLIST.md](MACHINE-SETUP-CHECKLIST.md)** - Setup guide (30 min quick start or 2-3 hour detailed)
3. **[hardware-requirements.md](hardware-requirements.md)** - Check your hardware compatibility
4. **[ai-integration.md](ai-integration.md)** - Understand the three AI engines

### Migrating from Another Machine?
1. **[MIGRATION-CHECKLIST.md](MIGRATION-CHECKLIST.md)** - Complete migration guide with pre/post checklists
2. **[MACHINE-SETUP-CHECKLIST.md](MACHINE-SETUP-CHECKLIST.md)** - Setup on new machine
3. **[hardware-requirements.md](hardware-requirements.md)** - Optimize for new hardware

---

## 📖 Core Documentation

### System Architecture
| Document | Description | For |
|----------|-------------|-----|
| **[architecture.md](architecture.md)** | System architecture overview | Developers, Architects |
| **[frontend-architecture.md](frontend-architecture.md)** | Angular frontend design | Frontend Devs |
| **[backend.md](backend.md)** | NestJS backend architecture | Backend Devs |
| **[data-models.md](data-models.md)** | Database schemas (MongoDB) | Backend Devs, DBAs |
| **[data-flow.md](data-flow.md)** | Data flow and communication | All Developers |

### API Documentation
| Document | Description | For |
|----------|-------------|-----|
| **[API_ENDPOINTS.md](../API_ENDPOINTS.md)** | Complete endpoint reference | API Consumers, Frontend Devs |
| **[backend-audio-assets.md](backend-audio-assets.md)** | Audio asset management | Backend Devs |
| **[backend-musicgen.md](backend-musicgen.md)** | MusicGen integration | AI/ML Engineers |

---

## 🤖 AI & Machine Learning

### Multi-Engine Architecture
| Document | Description | Topics Covered |
|----------|-------------|----------------|
| **[ai-integration.md](ai-integration.md)** | Multi-engine AI overview | Suno, Udio, MusicGen, Engine routing |
| **[hardware-requirements.md](hardware-requirements.md)** | Hardware specs & GPU config | CPU/RAM/GPU requirements, CUDA setup, Performance benchmarks |
| **[ollama-engine.md](ollama-engine.md)** | Ollama integration | Lyrics generation, Prompt engineering |
| **[ollama-setup.md](ollama-setup.md)** | Ollama installation | Setup, Configuration, Models |

### Engine Comparison
| Engine | Quality | Privacy | Speed | Cost | Free Tier |
|--------|---------|---------|-------|------|-----------|
| **Suno** | ⭐⭐⭐⭐⭐ | Cloud | Fast | API credits | 50 songs/day |
| **Udio** | ⭐⭐⭐⭐⭐ | Cloud | Fast | API credits | 3 songs/day |
| **MusicGen** | ⭐⭐⭐ | 100% Local | Medium-Slow | Free (uses hardware) | Unlimited |

See [ai-integration.md](ai-integration.md) for detailed comparison.

---

## 🔧 Setup & Configuration

### Initial Setup
| Document | Time | Description |
|----------|------|-------------|
| **[MACHINE-SETUP-CHECKLIST.md](MACHINE-SETUP-CHECKLIST.md)** | 30 min - 2.5 hrs | Complete setup guide with quick and detailed paths |
| **[setup-guide-high-performance.md](setup-guide-high-performance.md)** | 2-3 hours | Detailed setup for high-performance workstations |
| **[hardware-requirements.md](hardware-requirements.md)** | 15 min read | Hardware planning and optimization |

### Migration & Upgrades
| Document | Time | Description |
|----------|------|-------------|
| **[MIGRATION-CHECKLIST.md](MIGRATION-CHECKLIST.md)** | 5-9 hours | Moving to new hardware (includes backup, transfer, verification) |

### Quick Reference
```bash
# Quick Setup (30 minutes)
git clone <repo> && cd true-north-audio
pnpm install
python -m venv .venv && .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
copy .env.example .env  # Edit with your API keys
pnpm dev  # Start all services
```

---

## 🧪 Testing

### Testing Documentation
| Document | Description | Topics |
|----------|-------------|--------|
| **[TESTING-GUIDE.md](TESTING-GUIDE.md)** | Comprehensive testing guide | All engine tests, CI/CD, Benchmarks |

### Running Tests
```bash
# Fast mode (5-10 seconds)
bash scripts/test-all-engines.sh --fast

# Full suite with report
bash scripts/test-all-engines.sh --report

# Test specific engine
bash scripts/test-all-engines.sh --engine musicgen

# Manual Python tests
python tests/test_all_engines.py --verbose
```

See [TESTING-GUIDE.md](TESTING-GUIDE.md) for complete testing documentation.

---

## 🎨 Frontend

### Angular Application
| Document | Description | Topics |
|----------|-------------|--------|
| **[frontend.md](frontend.md)** | Frontend overview | Angular, Material Design 3, RxJS |
| **[frontend-architecture.md](frontend-architecture.md)** | Architecture details | Components, Services, State management |

### Key Frontend Features
- Material Design 3 with vibrant UI
- Engine selector (Suno, Udio, MusicGen)
- Real-time audio generation
- WebSocket for streaming updates
- Advanced parameter controls

---

## ⚙️ Backend

### NestJS Server
| Document | Description | Topics |
|----------|-------------|--------|
| **[backend.md](backend.md)** | Backend overview | NestJS, MongoDB, API architecture |
| **[backend-audio-assets.md](backend-audio-assets.md)** | Audio management | Storage, Retrieval, Serving |
| **[backend-musicgen.md](backend-musicgen.md)** | MusicGen integration | FastAPI proxy, Parameter passing |

### API Layers
1. **NestJS Backend** (port 3000) - Main API gateway
2. **FastAPI Python** (port 8000) - AI engine interface
3. **Ollama Proxy** (port 11434) - Request routing

---

## 📊 Data & Models

### Database & Schemas
| Document | Description | Topics |
|----------|-------------|--------|
| **[data-models.md](data-models.md)** | Data models | MongoDB schemas, Mongoose ODM |
| **[data-flow.md](data-flow.md)** | Data flow | Request/response flow, WebSocket |

### User Management
| Document | Description | Topics |
|----------|-------------|--------|
| **[user-management.md](user-management.md)** | Authentication & authorization | RBAC, JWT, OAuth (planned) |

---

## 🎵 Features & Roadmap

### Current Features
| Document | Description | Status |
|----------|-------------|--------|
| **[features.md](features.md)** | Feature list | Complete feature overview |

### Feature Highlights
- ✅ Multi-engine AI music generation (Suno, Udio, MusicGen)
- ✅ GPU acceleration for local generation
- ✅ ElevenLabs voice integration
- ✅ Advanced parameter controls (tempo, genre, mood, vocals)
- ✅ Real-time generation monitoring
- ✅ Audio playback and download

### Planned Features
| Document | Description | Status |
|----------|-------------|--------|
| **[video-roadmap.md](video-roadmap.md)** | Video feature planning | Future roadmap |
| **[video.md](video.md)** | Video integration | Planned |

---

## 🛠️ Development

### Coding Standards
- **Nx First**: All tasks via `nx run`, `nx run-many`, `nx affected`
- **Strict Linting**: ESLint, Prettier, Angular style guides
- **TypeScript**: Strict mode, no implicit any
- **Testing**: Unit tests, E2E tests, AI engine tests

### Workflow
```bash
# Lint all
pnpm nx run-many --target=lint --all

# Test all
pnpm nx run-many --target=test --all

# Build all
pnpm nx run-many --target=build --all

# Test AI engines
bash scripts/test-all-engines.sh
```

### Documentation Standards
- All endpoints documented in `API_ENDPOINTS.md`
- All features documented before merge
- Architecture decisions in `/docs`
- Code examples in docstrings

---

## 🆘 Troubleshooting

### Common Issues

**CUDA Not Detected**:
```bash
# Reinstall PyTorch with CUDA
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Port Already in Use**:
```bash
bash scripts/kill-all.sh
```

**Out of Memory**:
```env
# In .env file
MUSICGEN_MODEL=small  # Use smaller model
```

**Import Errors**:
```bash
.\.venv\Scripts\Activate.ps1  # Activate venv
pip install -r requirements.txt  # Reinstall
```

See individual documentation files for detailed troubleshooting.

---

## 📞 Support & Resources

### External Resources
- **AudioCraft**: https://github.com/facebookresearch/audiocraft
- **Suno AI**: https://suno.com/
- **Udio AI**: https://udio.com/
- **ElevenLabs**: https://elevenlabs.io/
- **Ollama**: https://ollama.ai/

### Internal Resources
- **Repository**: https://github.com/JeffreySanford/true-north-audio
- **Branch**: `vocal-integration` (current development)

---

## 📝 Documentation Updates

### Contributing to Documentation
1. Edit markdown files in `/docs`
2. Follow existing structure and formatting
3. Include code examples where appropriate
4. Update this index if adding new documents
5. Test all commands and code snippets
6. Update date in document footer

### Documentation Checklist for New Features
- [ ] Update `API_ENDPOINTS.md` if adding endpoints
- [ ] Update `features.md` with new feature
- [ ] Add usage examples to relevant docs
- [ ] Update architecture diagrams if needed
- [ ] Add tests to `TESTING-GUIDE.md`
- [ ] Update this index

---

## 📅 Documentation Metadata

**Last Updated**: November 5, 2025  
**Version**: 1.0 (Multi-Engine Architecture)  
**Maintainer**: Jeffrey Sanford  
**Repository**: true-north-audio  
**Branch**: vocal-integration

---

## 🗺️ Quick Navigation

### By Role
- **New Developer**: README → MACHINE-SETUP-CHECKLIST → architecture.md
- **Frontend Developer**: frontend-architecture.md → API_ENDPOINTS.md
- **Backend Developer**: backend.md → data-models.md → API_ENDPOINTS.md
- **AI/ML Engineer**: ai-integration.md → hardware-requirements.md → TESTING-GUIDE.md
- **DevOps**: MACHINE-SETUP-CHECKLIST → MIGRATION-CHECKLIST → hardware-requirements.md
- **QA Engineer**: TESTING-GUIDE.md → API_ENDPOINTS.md

### By Task
- **Setting up new machine**: MACHINE-SETUP-CHECKLIST.md
- **Migrating hardware**: MIGRATION-CHECKLIST.md
- **Adding new engine**: ai-integration.md → TESTING-GUIDE.md
- **Optimizing performance**: hardware-requirements.md
- **Debugging issues**: Troubleshooting sections in relevant docs
- **Testing changes**: TESTING-GUIDE.md

---

**Questions? Check the relevant documentation above or create an issue in the repository.**
