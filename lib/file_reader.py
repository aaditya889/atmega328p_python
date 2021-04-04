

def read_file_indefinite(file_name):
  queue = list()
  fd = open(file_name, 'r')
  queue.extend(fd.readlines())

  try:
    while True:
      queue.extend(fd.readlines())
      if len(queue) > 0:
        data = queue[0]
        del queue[0]
        yield data.strip('\n')
      else:
        yield None
  except KeyboardInterrupt:
    fd.close()
