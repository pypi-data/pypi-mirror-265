import time as _time

dump_dir = f'./llm_dump_{_time.strftime("%Y%m%d-%H%M")}.tar'

cache_dir = '~/llm_cache'  # optional, set None to disable cache

suffix_chat = '_chat.yaml'
suffix_completion = '.yaml'

stage = 'llm'
