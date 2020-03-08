**Activate the virtual environment**

```
source PyBlockChain-env/scripts/activate
```

**Install the dependencies**

```
pip install -r requirements.txt
```

**Running Tests**

```
python -m pytest backend/tests
```

**Run the API**

```
python -m backend.app
```

**To run a peer instance**

```
export PEER=True && python -m backend.app
```