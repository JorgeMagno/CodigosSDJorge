import operator
import socket		 	 # Import socket module
import sys
import xml.etree.cElementTree as ET

ops = { '+': operator.add,		#usando a importação da biblioteca 'operator' ligando cada caractere a uma operação
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
}

def eval_expression(tokens, stack):					#função responsável por realizar o cálculo recebendo dois parâmetros, uma lista com cada elemento da expressão e outra lista vazia
    for token in tokens:
        if set(token).issubset(set("0123456789.")):			#condição criada para caso o elemento for um número ser adicionado a lista vazia
            stack.append(float(token))					#adiciona o elemento a lista vazia
        elif token in ops:						#condição criada para o elemento for um dos operadores
            if len(stack) < 2:						#condição que verifica se a expressão tem pelo 3 elementos
                stack = ['Parâmetros Insuficientes ou Escrita Errada']
                return stack
            a = stack.pop()		#retira o último número adicionado a lista e armazena na variável 'a'
            b = stack.pop()		#realiza o mesmo só que armazenando a variável 'b'
            op = ops[token]		#armazena o operador para variavél 'op'
            stack.append(op(b,a))	#realiza a operação e adiciona o resultado da mesma na lista
        else:				#condição paa mandar uma mensagem de erro qualquer que tenha havido
            stack ['Erro!']		
            return stack
    return stack			#retorna o resultado da função

if __name__ == '__main__':
    s = socket.socket() 	  		  # Criação do socket
    host = socket.gethostname()                     # pega o nome da máquina local
    port = 3000					#fornece o número da porta
    s.bind((host, port)) 			 # liga o socket ao endereço e a porta
    s.listen()					# espera um cliente se conectar
    stack = []					#criação de uma lista vazia
    stackxml = [] 			         #criação de uma lista vazia que vai armazenar o que for extraido do xml
    print("Servidor Funcionando!")
    while True:						#laço para manter o servidor sempre ativo
      c, addr = s.accept() 		# estabelecendo conexão com o cliente
      print('Conexão de ', addr)
      while True:   					#laço que mantém a conexaõ ativa com cliente até ele decidir sair
        equation=c.recv(1024).decode('utf-8')		#recebe os a string vinda do cliente no formato utf8, os decodifica e armazena em 'equation'
        root = ET.fromstring(equation)			#lendo os dados xml da string
        for elem in root:				#laço para adicionar os elementos texto no xml para 'stackxml'
            for subelem in elem:
                stackxml.append(subelem.text) 		#adicinona o elemento do tesxto ao 'stackxml'
        if stackxml[0] == "Q" or stackxml[0] == "q":	#condição que verifica se o usuário mandou uma mensagem de fechamento de conexão
          c.send("Quit".encode())
          stack = []
          stackxml = []
          print ("Adeus!")
          break
        else:
          stack = eval_expression(stackxml, stack)	#chama a função que realiza o cálculo e armazena o resultado
          c.send(str(stack).encode())			#envia a resposta do cálculo para o cliente
          stack = []					#esvazia a lista após o envio do resultado
          stackxml = []
      c.close()				#fecha a conexão quando usuário decidir sair
