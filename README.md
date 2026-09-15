# virtual-fly-brain-puppy

Windows용 독립 실행형(패키징 지원) **가상 초파리 뇌 강아지 시뮬레이터**입니다.

## 포함된 기능
- 3000+ 뉴런 / 548,000+ 시냅스 규모의 connectome 시뮬레이션 코어
- FlyEM/malecns 형식 CSV 자동 로드 (`data/malecns_connectome.csv`)
- PyQt5 GUI: 재생/일시정지, 속도 슬라이더, 연결망 복잡도 설정
- 3D 강아지 아바타 + 환경(장애물/먹이/빛) + 행동 로그
- 실시간 신경활동(칼슘) 히트맵 시각화
- Windows 배포 파일: PyInstaller spec + Inno Setup 스크립트
- 한글 사용자 매뉴얼: `docs/사용자_매뉴얼_ko.md`

## 실행 (개발 환경)
```bash
pip install -r requirements.txt
python main.py
```

## Windows .exe 빌드
1. `build_windows.bat` 실행
2. `installer.iss`를 Inno Setup에서 빌드하여 설치 프로그램 생성

## GitHub Release로 Windows 설치파일 배포
이 저장소에는 Windows에서 자동 빌드/릴리스하는 워크플로우가 포함되어 있습니다.

1. GitHub 저장소의 **Actions** 탭에서 `Build and Release Windows Installer` 실행
2. `version` 입력 (예: `1.0.0`)
3. 완료 후 **Releases** 탭에서 `VirtualFlyBrainPuppyInstaller_<version>.exe` 다운로드

릴리스 설치파일은 Python 미설치 환경(Windows 10/11)에서도 바로 설치/실행 가능합니다.

## Connectome 데이터 준비
실제 데이터 사용 시 `data/malecns_connectome.csv`를 배치하세요.
필수 컬럼은 `data/connectome_source_note.txt`를 참고하세요.
