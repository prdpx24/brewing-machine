# brewing-machine
> A brewing-machine for fun & profit!

# Installation
* Clone the repo
```bash
git clone https://github.com/prdpx24/brewing-machine
```
# Tests
* Automated Testing
```bash
cd brewing-machine/
python3 tests.py
```

* Manual Testing
```bash
cd brewing-machine/
# driver application(app.py) is randomly choosing n beverage out of all offered beverages by brewing machine
# and executing all of them using python threads, hence different output on same testcase
python3 app.py --json sample_input.json
python3 app.py --json testcases/input_1.json
python3 app.py --json testcases/input_2.json
```
# Demo
<img src="https://i.imgur.com/Vvy0Gqy.gif">

# Note
* Executing `app.py` with python2 may show some extra newlines on `STDOUT` because `print` function in python2.7 is not thread safe.
