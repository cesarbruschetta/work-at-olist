# Test of aplication

## Run unittest

```bash
$ cd /path/to/env/billing_phonecalls/app
$ python manage.py test -v 2
```

## Run analyze code by pylint

```bash
$ cd /path/to/env/billing_phonecalls/app
$ ../bin/pylint billing_phonecalls/*
```

## Run analyze code by pylint

```bash
$ cd /path/to/env/billing_phonecalls/app
$ ../bin/pylint billing_phonecalls/*
```

## Run analyze code by pep8

```bash
$ cd /path/to/env/billing_phonecalls/app
$ ../bin/flake8 billing_phonecalls/*
```

* To format code to pep8 rules

`$ ./bin/autopep8 --in-place --aggressive --aggressive -r billing_phonecalls/`

## Run Coverage report

After wheels the unit tests execute the command below

```bash
$ cd /path/to/env/billing_phonecalls/app
$ ../bin/coverage html
```

The command generate a folder called `htmlcov` and you can open the `index.html` in your browser to view the report


## Analyze by Coverage

|Module|statements|missing|excluded|coverage|
|--- |--- |--- |--- |--- |
|Total|426|152|0|64%|
|billing_phonecalls/__init__.py|0|0|0|100%|
|billing_phonecalls/core/__init__.py|0|0|0|100%|
|billing_phonecalls/core/admin.py|17|17|0|0%|
|billing_phonecalls/core/apps.py|3|3|0|0%|
|billing_phonecalls/core/migrations/0001_initial.py|7|0|0|100%|
|billing_phonecalls/core/migrations/__init__.py|0|0|0|100%|
|billing_phonecalls/core/models/__init__.py|0|0|0|100%|
|billing_phonecalls/core/models/billing.py|21|16|0|24%|
|billing_phonecalls/core/models/phone_calls.py|59|37|0|37%|
|billing_phonecalls/core/models/price.py|19|17|0|11%|
|billing_phonecalls/core/pricing.py|66|24|0|64%|
|billing_phonecalls/core/serializers.py|41|1|0|98%|
|billing_phonecalls/core/tests/__init__.py|0|0|0|100%|
|billing_phonecalls/core/tests/tests_models.py|39|0|0|100%|
|billing_phonecalls/core/tests/tests_pricing.py|20|0|0|100%|
|billing_phonecalls/core/tests/tests_views.py|60|3|0|95%|
|billing_phonecalls/core/urls.py|3|0|0|100%|
|billing_phonecalls/core/utils.py|16|7|0|56%|
|billing_phonecalls/core/views.py|25|0|0|100%|
|billing_phonecalls/settings.py|23|23|0|0%|
|billing_phonecalls/urls.py|3|0|0|100%|
|billing_phonecalls/wsgi.py|4|4|0|0%|