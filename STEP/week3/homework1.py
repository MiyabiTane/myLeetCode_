def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1


def readMalti(line, index):
  token = {'type' : 'MALTI'}
  return token, index + 1


def readDevis(line, index):
  token = {'type' : 'DEVIS'}
  return token, index + 1


def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
    elif line[index] == '+':
      (token, index) = readPlus(line, index)
    elif line[index] == '-':
      (token, index) = readMinus(line, index)
    elif line[index] == '*':
      (token, index) = readMalti(line, index)
    elif line[index] == '/':
      (token, index) = readDevis(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  #print(tokens)
  return tokens


def firstEvaluate(tokens):

  def checker(tokens, index):
    if tokens[index - 1]['type'] != 'NUMBER' or tokens[index + 1]['type'] != 'NUMBER':
        print('Invalid syntax')
        exit(1)

  tokens.insert(0, {'type': 'PLUS'})  # Insert a dummy '+' token
  index = 0
  while index < len(tokens):
    if tokens[index]['type'] == 'MALTI':
      checker(tokens, index)
      new_number = tokens.pop(index - 1)['number'] * tokens.pop(index)['number']
      tokens.insert(index - 1, {'type': 'NUMBER', 'number': new_number}) 
      tokens.pop(index)
    elif tokens[index]['type'] == 'DEVIS':
      checker(tokens, index)
      if tokens[index + 1]['number'] == 0:
        print("cannot devide by 0")
        exit(1)
      new_number = tokens.pop(index - 1)['number'] / tokens.pop(index)['number']
      tokens.insert(index - 1, {'type': 'NUMBER', 'number': new_number})
      tokens.pop(index)
    else:
      index += 1 
    
  #print(tokens)
  return tokens


def secondEvaluate(new_tokens):
  answer = 0
  index = 1
  while index < len(new_tokens):
    if new_tokens[index]['type'] == 'NUMBER':
      if new_tokens[index - 1]['type'] == 'PLUS':
        answer += new_tokens[index]['number']
      elif new_tokens[index - 1]['type'] == 'MINUS':
        answer -= new_tokens[index]['number']
      else:
        print('Invalid syntax')
        exit(1)
    index += 1
  return answer


def test(line):
  if len(line) == 0:
    print("please input some numbers")
    return None
  tokens = tokenize(line)
  new_tokens = firstEvaluate(tokens)
  actualAnswer = secondEvaluate(new_tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" %
          (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  test("")
  test("1")
  test("1+2")
  test("12+3")
  test("1.0+2")
  test("1-3")
  test("2.0-13")
  test("3-14+4.0")
  test("2*3")
  test("4.2*9")
  test("2*2*2")
  test("3*5.9+2")
  test("6.0-4*2")
  test("8/9")
  test("6/3.0/4")
  test("6.0/4")
  test("4*5-7.0/3+2")
  test("3/0")
  test("3+2+4.0*4-4/2.0")
  print("==== Test finished! ====\n")


runTest()

"""
while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  new_tokens = first_evaluate(tokens)
  answer = second_evaluate(new_tokens)
  print("answer = %f\n" % answer)
"""