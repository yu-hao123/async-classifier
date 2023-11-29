# async-classifier
Library in Python for classifying respiratory asynchronies

## Usage

`classify.py` contains the methods for detecting and classifying the following asynchronies:

- Ineffective Effort (IEE)
- Double Trigger (DT)
- Auto Trigger (AT)
- Reverse Trigger Single and Double (RTs, RTd)
- Early Cycling (EC)
- Late Cycling (LC)

All of the methods above expects `ins_marks` and `exp_marks` arrays with the same size, and the same goes with `pmus_start_marks` and `pmus_finish_marks`.
Classifers also expects that `ins_marks[0] < exp_marks[0]` and `pmus_start_marks[0] < pmus_finish_marks[0]`.

`example.py` shows these methods applied to two distinct ventilation datasets (VCV and PCV).

