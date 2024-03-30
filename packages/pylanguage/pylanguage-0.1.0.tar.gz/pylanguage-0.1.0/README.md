# pylanguage

Translation assistant for Python

## Usage

### Install

```bash
pip install --user pylanguage
```

### Importing

```python
from pylanguage.translator import Translator as T
```

### Use in code

Suppose your project directory is of following structure:

```
myproject
 |
  ---- src/
 |   |
 |    --- __init__.py
 |    --- myfile.py    # Uses pylanguage
 |
  ---- translations
      |
       ---- base.json # base translations
      |
       ---- en_US.json # English US translations
```

#### Step 1: Import the library

```python
from pylanguage.translator import Translator as T
```

#### Step 2: Create a translator object

Here, `myfile.py` uses the translations. So, under the import statement and before any strings, create the translations object.
Here using `en_US` as an example,

```python
import pathlib
from pylanguage.translator import Translator as T

proj_dir = str(pathlib.Path(__file__).parent.resolve())
translation_dir = str(pathlib.Path().joinpath(proj_dir, 'translations'))

p = T(base_file = 'base.json', lang_code = 'en_US', lang_dir = translation_dir)
```

#### Step 3: Use the `get()` method

Now, use the `get()` method of the `Translator` object.

Complete code of the previous example:

```python
import pathlib
from pylanguage.translator import Translator as T

proj_dir = str(pathlib.Path(__file__).parent.resolve())
translation_dir = str(pathlib.Path().joinpath(proj_dir, 'translations'))

p = T(base_file = 'base.json', lang_code = 'en_US', lang_dir = translation_dir)

print(p.get("Hello World"))
```


### The translations files

Both base file and language specific files use the following spec. Do note however that the base file will have same keys and values.

For the example above, both `base.json` and `en_US.json` will have the following content:

```json
{
  "Hello World": "Hello World"
}
```


## License

See [LICENSE file.](./LICENSE)

Tl;dr: This project uses MIT License.

## Complete docs

See [Documentation](https://aerocyber.github.io/pylanguage/docs)