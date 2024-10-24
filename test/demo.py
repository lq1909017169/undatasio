
# from undatasio.undatasio import undatasio
from undatasio.undatasio.undatasio import UnDatasIO

undatasio = UnDatasIO(token='025ae1da7598456daa802fef7873e31b', task_name='文本解析')

print(undatasio.show_version())
print(undatasio.get_result_to_files(['初中数学浙江中考数学真题-7.pdf'], 'v18'))