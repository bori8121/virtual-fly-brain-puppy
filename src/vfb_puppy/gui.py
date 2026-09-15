from __future__ import annotations

from pathlib import Path
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

from .connectome import load_connectome
from .brain import FlyBrainSimulator
from .behavior import BehaviorMapper
from .environment import PuppyEnvironment, PuppyPose


class FlyBrainPuppyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("가상 초파리 뇌 강아지")
        self.resize(1300, 760)

        self.connectome = load_connectome(complexity="full")
        self.brain = FlyBrainSimulator(self.connectome)
        self.mapper = BehaviorMapper(self.connectome.neuron_ids.size)
        self.env = PuppyEnvironment()
        self.pose = PuppyPose()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.tick_ms = 33

        self._build_ui()
        self._reset_scene()

    def _build_ui(self):
        root = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(root)

        self.view3d = gl.GLViewWidget()
        self.view3d.setCameraPosition(distance=15, elevation=20, azimuth=45)
        layout.addWidget(self.view3d, stretch=3)

        right = QtWidgets.QVBoxLayout()
        layout.addLayout(right, stretch=2)

        controls = QtWidgets.QGroupBox("시뮬레이션 제어")
        c_lay = QtWidgets.QFormLayout(controls)

        self.play_btn = QtWidgets.QPushButton("재생")
        self.play_btn.clicked.connect(self.toggle_play)
        c_lay.addRow(self.play_btn)

        self.speed_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(3)
        self.speed_slider.valueChanged.connect(self.update_speed)
        c_lay.addRow("속도", self.speed_slider)

        self.complexity = QtWidgets.QComboBox()
        self.complexity.addItems(["full", "medium", "core"])
        self.complexity.currentTextChanged.connect(self.reload_complexity)
        c_lay.addRow("연결망 복잡도", self.complexity)
        right.addWidget(controls)

        self.heatmap = pg.ImageView(view=pg.PlotItem())
        self.heatmap.ui.histogram.hide()
        self.heatmap.ui.roiBtn.hide()
        self.heatmap.ui.menuBtn.hide()
        right.addWidget(self.heatmap, stretch=2)

        self.log = QtWidgets.QTextEdit()
        self.log.setReadOnly(True)
        right.addWidget(self.log, stretch=1)

        self.setCentralWidget(root)

    def _reset_scene(self):
        self.view3d.clear()
        grid = gl.GLGridItem()
        grid.setSize(10, 10)
        self.view3d.addItem(grid)

        self.puppy_body = gl.GLMeshItem(
            meshdata=gl.MeshData.sphere(rows=18, cols=18, radius=0.9),
            smooth=True,
            color=(1.0, 0.82, 0.62, 1.0),
            shader="shaded",
        )
        self.puppy_head = gl.GLMeshItem(
            meshdata=gl.MeshData.sphere(rows=16, cols=16, radius=0.55),
            smooth=True,
            color=(1.0, 0.89, 0.72, 1.0),
            shader="shaded",
        )
        self.view3d.addItem(self.puppy_body)
        self.view3d.addItem(self.puppy_head)

        for x, y in self.env.food:
            food = gl.GLMeshItem(meshdata=gl.MeshData.sphere(rows=8, cols=8, radius=0.2), color=(0.2, 0.8, 0.2, 1), shader="shaded")
            food.translate(float(x), float(y), 0.2)
            self.view3d.addItem(food)

        for x, y in self.env.obstacles:
            obs = gl.GLMeshItem(meshdata=gl.MeshData.cylinder(rows=8, cols=20, radius=[0.25, 0.25], length=1.0), color=(0.7, 0.2, 0.2, 1), shader="shaded")
            obs.translate(float(x), float(y), 0.5)
            self.view3d.addItem(obs)

    def toggle_play(self):
        if self.timer.isActive():
            self.timer.stop()
            self.play_btn.setText("재생")
        else:
            self.timer.start(self.tick_ms)
            self.play_btn.setText("일시정지")

    def update_speed(self, value: int):
        self.tick_ms = max(1, 34 - value * 3)
        if self.timer.isActive():
            self.timer.start(self.tick_ms)

    def reload_complexity(self, level: str):
        running = self.timer.isActive()
        if running:
            self.timer.stop()
        self.connectome = load_connectome(complexity=level)
        self.brain = FlyBrainSimulator(self.connectome)
        self.mapper = BehaviorMapper(self.connectome.neuron_ids.size)
        self.log.append(f"[설정] 연결망 복잡도 변경: {level}")
        if running:
            self.timer.start(self.tick_ms)

    def tick(self):
        sensory = self.env.sensory_vector(self.pose, self.connectome.neuron_ids.size)
        state = self.brain.step(sensory)
        command = self.mapper.to_motor_command(state.spikes, state.calcium)
        self.pose = self.env.apply_motor(self.pose, command.forward, command.turn, command.head_tilt)
        self._update_avatar()

        heat = self.brain.neural_heatmap(30)
        self.heatmap.setImage(heat, autoLevels=False)

        msg = (
            f"pos=({self.pose.x:.2f},{self.pose.y:.2f}) "
            f"turn={command.turn:.3f} forward={command.forward:.3f}"
        )
        self.log.append(msg)
        if self.log.document().blockCount() > 120:
            cursor = self.log.textCursor()
            cursor.movePosition(cursor.Start)
            cursor.select(cursor.BlockUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()

    def _update_avatar(self):
        self.puppy_body.resetTransform()
        self.puppy_head.resetTransform()

        self.puppy_body.translate(self.pose.x, self.pose.y, 0.9)
        self.puppy_body.rotate(np.degrees(self.pose.heading), 0, 0, 1)

        hx = self.pose.x + np.cos(self.pose.heading) * 0.95
        hy = self.pose.y + np.sin(self.pose.heading) * 0.95
        self.puppy_head.translate(hx, hy, 1.2 + self.pose.head_tilt * 0.25)
        self.puppy_head.rotate(np.degrees(self.pose.heading), 0, 0, 1)


def run_app():
    app = QtWidgets.QApplication([])
    win = FlyBrainPuppyWindow()
    win.show()
    app.exec_()
