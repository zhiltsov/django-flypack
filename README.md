# Django Flypack

Модуль позволяет создавать в Django статичные страницы, блоки текста, меню.

## Install
В файле `settings.py` добавить:

```python
INSTALLED_APPS = (
    ...
    'flypack',
    'flypack.templatetags',
)

FLYMENU_EXTENDED = (
    ('your_extended_menu', 'Items'),
)
```

`your_extended_menu` - массив для вывода динамического древовидного меню. Формат аналогичен `flypack.models.Menu`.

## Template tag
### get_flyblock

**Syntax**:
```python
{% get_flyblock ['code'] as context_name %}
```
or simple:
```python
{% get_flyblock ['code'] %}
```

**Example usage**:
```python
{% get_flyblock general as general_block %}
```
or simple:
```python
{% get_flyblock general %}
```

### get_flymenu

**Syntax**:
```python
{% get_flymenu ['code'] as context_name %}
```

**Example usage**:
```python
{% get_flymenu general as general_menu %}
```

