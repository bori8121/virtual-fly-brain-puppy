# Virtual Fly Brain Puppy 사용자 매뉴얼 (한글)

## 1. 설치 (Windows)
1. Python 없이 배포하려면 `build_windows.bat` 실행 후 생성된 `dist` 폴더를 준비합니다.
2. Inno Setup에서 `installer.iss`를 열어 빌드하면 설치 파일(`VirtualFlyBrainPuppyInstaller.exe`)이 생성됩니다.
3. 생성된 설치 파일을 더블클릭해 설치합니다.

## 2. 실행
- 시작 메뉴 또는 바탕화면의 **Virtual Fly Brain Puppy** 아이콘을 더블클릭합니다.

## 3. 화면 구성
- **재생/일시정지 버튼**: 시뮬레이션 시작/정지
- **속도 슬라이더**: 시뮬레이션 시간 배율 조정
- **연결망 복잡도**: full(3000+), medium, core
- **3D 뷰**: 마우스로 회전/줌
- **활동 히트맵**: 실시간 칼슘 활동
- **행동 로그**: 위치/회전/운동 신호 기록

## 4. Connectome 데이터
- 실제 FlyEM/malecns 데이터가 있으면 `data/malecns_connectome.csv`로 저장합니다.
- CSV 스키마:
  - `pre_neuron`, `post_neuron`: 뉴런 ID
  - `weight`: 시냅스 가중치
  - `pre_neuropil`, `post_neuropil`: neuropil ID

## 5. 오프라인 사용
- 설치 후 네트워크 없이 실행 가능합니다.
