# smart-car-control
Smart car control project with PID simulation, STM32 and Python visualization.

## 运行 PID / 电机仿真

在本地仓库根目录打开终端（Python 3.9 或更新版本）：

```bash
python -m pip install -r simulation/requirements.txt
python simulation/main.py
```

会显示电机速度曲线和目标速度 100 的虚线，同时保存
`simulation/pid_response.png`。关闭图像窗口后程序结束。
原有 `simulation/main.py`、`pid.py`、`motor.py` 的位置保持不变。
PID 和电机模型公式、默认增益、步长 0.01 秒、500 次更新均保持不变。

也支持从根目录运行 `python -m simulation.main`，或进入 `simulation` 后运行
`python main.py`。请运行完整的 `main.py` 文件，不要只运行选中的几行。

没有图形桌面、窗口不显示或只需要图片时：

```bash
python simulation/main.py --no-show
```

该命令使用非交互式绘图后端，直接打开生成的 PNG 即可查看曲线。
可用 `--save result.png` 指定图片路径（相对于当前终端目录，父目录需已存在）。
每次运行会覆盖同名图片。

调整增益示例：

```bash
python simulation/main.py --kp 3 --ki 0.2 --kd 0.05
```

## 为什么原代码没有曲线

截至提交 `2cb58a0`，`main.py` 只在循环中打印速度，没有记录历史数据，
也没有导入 Matplotlib、调用 `plot()` 或 `show()`；它本身不会创建图像窗口。
修复版记录初始状态和每次更新后的速度，共 501 个数据点，先画线并保存图片，
再调用阻塞式 `show()`。更新后的时间标记为 `(i + 1) * dt`，与实际采样时刻一致。
仅凭远端代码无法确认本地未上传的绘图修改为什么出现空白窗口。

默认参数在 5 秒结束时速度约为 70，尚未收敛到 100，这是当前模型和参数的仿真结果，
不代表绘图失败。本次修复不重新调参。
如果大幅增大 Kd 导致正负交替振荡，需要检查离散仿真稳定性；
微分项会把相邻误差之差除以 0.01，较大的 Kd 可能使控制量剧烈变化。
非有限的参数或发散至非有限数值时，程序会明确报错。

