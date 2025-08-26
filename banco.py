from datetime import datetime
from pydoc import cli

#Gustavo Atui
#Lucas Cabral 



#dicionario para conseguir armazenar os clientes em base no seu cnpj
clientes= {}


#para obter o arquivo é preciso criar um arquivo chamado "clientes.txt"
arq=open("clientes.txt", "r")

for linha in arq.readlines():
    if len(linha) <= 1:
        continue    
    info = linha.split(" ! ")
    CNPJ = int(info[0])
    saldo = float(info[3])
    saldoinv = float(info[5])
    extrat = info[6]
    #utilizamos a funçao "Eval" para transformar string em lista
    extrato=eval(extrat)
    clientes[CNPJ] = [info[1],info[2],saldo,info[4],saldoinv,extrato]
del arq

# função para criar novo cliente
def novo():
    # com os inputs voce coloca as infos para criar sua conta 
    razao=input("Digite a sua razão social: ")
    CNPJ=int(input("Digite seu CNPJ: "))
    # quando voce tenta registrar um cnpj ja cadastrado no banco ele ira retornar a função
    if CNPJ in clientes:
         print("CNPJ ja registrado")
         return
    nomeusuario=input("Digite seu nome de usuario: ")
    tipoconta=input("Digite seu tipo de conta (Comum ou Plus): ")
    valorinicial=float(input("Digite o valor inicial da sua conta: "))
    senha=input("Digite sua Senha: ")
    saldopoup = float(input("Digite o valor inicial da sua poupança: "))
    # poupanca.append(saudopoup) ira adicionar o valor investido no saldo da poupanca 
    
    # o clientes[CNPJ] é um dicionario de cnpj onde cada cnpj tem uma lista com as infos dos clientes 
    clientes[CNPJ] =[nomeusuario,tipoconta,valorinicial,senha,saldopoup,[]]
    # diferencia o tipo de conta (Comum ou Plus) e se colocar um tipo de conta que nao existe ira aparecer tipo de conta invalido
    #SO IRA FUNCIONAR CASO DIGITE "Plus" ou "Comum" , ambas precisam começar com letra maiscula para funcionar
    if tipoconta == "Comum":
        clientes[CNPJ] =[nomeusuario,tipoconta,valorinicial,senha, saldopoup,[]]
    elif tipoconta == "Plus":
        clientes[CNPJ] =[nomeusuario,tipoconta,valorinicial,senha, saldopoup,[]]
    else:
        print("Tipo de conta inválido")

# funcao para apagar o cliente
def apaga():
    #input para colocar seu cnpj
    CNPJ=int(input("Digite seu CNPJ: "))
    # se o cnpj estiver dentro do dicionario de clientes a funcao ira proseguir com o encerramento da conta caso contrario ira aparecer CNPJ nao encontrado
    if CNPJ in clientes:
        # com esse input voce ira confirmar se quer mesmo apagar a conta caso contrario ela nao ira ser apagada 
        a = input("Deseja realmente apagar sua conta ? ")
        if a == "sim" or a == "s":
            del clientes[CNPJ]
            print("sua conta foi cancelada com sucesso")
        elif a == "não" or a == "n":
            print("Sua conta não foi cancelada")
    else:
        print("CNPJ não encontrado")
# funcao para listar os clientes
def listar():
    print("listar clientes")
    # se o CNPJ e as infos dos clientes estiverem dentro do dicionario clientes ira aparecer as infos de todos clientes cadastrados
    for CNPJ,itens in clientes.items():
        print(CNPJ,itens)
# funcao de debito
def deb():
    #  os  dois primeiros inputs que sao do cnpj e da senha irao ser verificados, se o cnpj existir e a senha for compativel deste cnpj voce conseguira executar o debito e o terceiro input é para saber o valor que sera debtado
    CNPJ=int(input("Digite seu CNPJ: "))
    senha=input("Digite sua Senha: ")
    valordeb=float(input("Digite o valor para ser debitado: "))
    
    #debito so ocorre se o cnpj estiver dentro de clientes e se a senha for igual a do cnpj digitado
    # é verificado o tipo de conta, o saldo da conta e o valor que sua conta pode ficar negativada que depende de qual tipo de conta voce escolheu  
    if CNPJ in clientes and senha == clientes[CNPJ][3]:
        tipoconta = clientes[CNPJ][1]
        valorconta = clientes[CNPJ][2]
        valormax = clientes[CNPJ][4]
        taxa = 0
        # se a conta for Comum é cobrado uma taxa de 0.05 e se a conta for Plus é cobrado uma taxa de 0.03 
        if tipoconta == "Comum":
            taxa = 0.05
        elif tipoconta == "Plus" :
            taxa = 0.03
        # se o valor para ser debitado somado com a taxa ultrapassar do valor que pode ficar negativado o debito nao ira ocorrer
        if valorconta - valordeb - (valordeb*taxa) < valormax:
            print("Valor do débito passou o limite permitido para esta conta")
        # se o valor para ser debitado somado com a taxa nao ultrapassar do valor que pode ficar negativado o debito ira ocorrer e logo em seguida o valor do debito sera debitado da sua conta 
        else:
            clientes[CNPJ][2] = clientes[CNPJ][2] -valordeb - (valordeb*taxa)
            data = datetime.now()
            histext = f"Data: {data.day}/{data.month}/{data.year}   {data.hour}:{data.minute}:{data.second} -{valordeb} Tarifa: {valordeb*taxa} Saldo: {clientes[CNPJ][2]}"
            clientes[CNPJ][5].append(histext)
            print("Débito realizado com sucesso")
    else:
        print("Erro")
        return
# funcao de deposito
def dep():
    #o primeiro input voce coloca seu cnpj e logo em seguida ele sera verificado se esta dentro do dicionario clientes e no segundo voce coloca o valor para ser depositado se o cnpj estiver dentro do dicionario ele ele adicionar o valor que foi colocado para deposito caso contrario ira acontecer um erro( que é o cnpj nao encontrado)
    CNPJ=int(input("Digite seu CNPJ: "))
    valordep=float(input("Digite o valor para depositar: "))
    if CNPJ in clientes:
        clientes[CNPJ][2] = valordep + clientes[CNPJ][2]
        data = datetime.now()
        histext =  f"Data: {data.day}/{data.month}/{data.year}   {data.hour}:{data.minute}:{data.second} +{valordep} Tarifa: 0.00 Saldo: {clientes[CNPJ][2]}"
        clientes[CNPJ][5].append(histext)
        print("Depósito realizado com sucesso")
    else:
        print("Erro")
        return
# funçao extrato
def ext():
    # voce consegue visualizar o extrato somente se o cnpj estiver dentro de clientes e se a senha for igual a do cnpj 
    CNPJ=int(input("Digite seu CNPJ: "))
    senha=input("Digite sua Senha: ")
    # verifica se o cnpj esta dentro do dicionario e se a senha é igual do cnpj digitado 
    if CNPJ in clientes and senha == clientes[CNPJ][3]:
    #pega o tipo de conta e o seu saldo dentro da lista de cnpj e coloca em 2 outras variaveis 
        tipoconta = clientes[CNPJ][1]
        valorconta = clientes[CNPJ][2]
        # se a conta for Comum mostra o saldo disponivel, o saldo neg permitido que é de -1000  e a taxa de debto
        if tipoconta == "Comum":
            print("Historico do Extrato:",clientes[CNPJ][5])
            print("Saldo negativo permitido: R$: -1000.00")
            print("Taxa de débito: 5%")
        # se a conta for Plus mostra o saldo disponivel, o saldo neg permitido que é de -5000  e a taxa de debto
        elif tipoconta == "Plus":
            print("Historico do Extrato:",clientes[CNPJ][5])
            print("Saldo negativo permitido: R$: -5000.00")
            print("Taxa de débito: 3%")
        #caso se a senha ou o cnpj estiverem errado nao consegue visualizar o extrato
        else:
            print("Erro")
            return
# funcao de transferencia entre contas 
def transfentrecontas():
    # os dois primeiros inputs sao o cnpj e senha de quem vai fazer a tranferencia que logo depois é verificado se cnpj esta dentro de clientes e se a senha for igual a do cnpj
    # o terceiro input é o cnpj do destinatario da transferencia que logo depois é verificado se ele esta dentro do dicionario clientes
    # o quarto input é o valor da transferencia  
    CNPJ=int(input("Digite seu CNPJ: "))
    senha=input("Digite sua Senha: ")
    CNPJdest=int(input("Digite o CNPJ do destino: "))
    valor=float(input("Digite o valor da transferencia: "))
    #verifica o cnpj e a senha de quem faz a transferencia
    if CNPJ in clientes and senha == clientes[CNPJ][3]:
        #verifica se o cnpj do destinatario esta em clientes 
        if CNPJdest in clientes:
            # a transferencia ira ocorrer se o saldo for maior ou igual o valor da transferencia 
            if clientes[CNPJ][2] >= valor:
                # o valor da transferencia é debitado da conta de quem fez e depositado na conta do destinatario
                clientes[CNPJ][2] = clientes[CNPJ][2] - valor
                clientes[CNPJdest][2] = clientes[CNPJdest][2] + valor
                data=datetime.now()
                histext = f"Data: {data.day}/{data.month}/{data.year}   {data.hour}:{data.minute}:{data.second} -{valor} Tarifa: 0.00 Saldo: {clientes[CNPJ][2]}"
                histextdest=f"Data: {data.day}/{data.month}/{data.year}   {data.hour}:{data.minute}:{data.second} +{valor} Tarifa: 0.00 Saldo: {clientes[CNPJdest][2]}"
                ext = clientes[CNPJ][5]
                ext.append(histext)
                clientes[CNPJdest][5].append(histextdest)
                print("Transferencia realizada")
            else:
                print("Saldo insufuciente para tranferencia")
        else:
            print("CNPJ do destino nao encontrado")
    else:
        print("Erro")
        return
             
                 

#funcao de investimento
def invest():
 #  os  dois primeiros inputs que sao do cnpj e da senha irao ser verificados, se o cnpj existir e a senha for compativel deste cnpj voce conseguira realizar o investimento
    CNPJ = int(input("Digite seu CNPJ : "))
    senha = input("Digite a sua senha: ")
    #valor que vai ser investido
    valor=float(input("Digite o valor que sera colocado na poupança: "))
    #data do investimento
    dia = int(input("Digite o dia do investimento: "))
    mes= int(input("Digite o mes do investimento: "))
    ano= int(input("Digite o ano do investimento: ")) 
    #data do investimento
    datapoup = datetime(ano,mes,dia)
    #data atual
    data = datetime.now()
    #tempo do investimento
    tempo = data - datapoup
    if tempo.days//30 > 1:

        time=tempo.days/30
        #verifica se o cnpj esta em clientes e se a senha é igual a senha do cnpj digitado
        if CNPJ in clientes and senha == clientes[CNPJ][3]:
            #investimento so é realizado se o saldo for maior ou igual que o valor do investimento 
            clientes[CNPJ][2] >= valor 
            #tira o dinheiro da conta corrente e coloca na conta de investimento
            clientes[CNPJ][2] = clientes[CNPJ][2] - valor 
            clientes[CNPJ][4] = clientes[CNPJ][4] + valor
            #Formula dos juros compostos com taxa de 5% ao mes 
            valorinvest = clientes[CNPJ][4] * (1+0.005) ** time
            rendimento = valorinvest - valor
            #quando rende dinheiro no investimento vai para conta de investimentos 
            clientes[CNPJ][4] = clientes[CNPJ][4] + rendimento
            clientes[CNPJ][4] = round(clientes[CNPJ][4],2)
            print("Investimento realizado com sucesso")      
        else:
            print("Erro")
            return
    else:
        print("Pouco tempo")

def sair():
    arq= open("clientes.txt", "w")
    string = ""
    for x,y in clientes.items():
        string = str(x) + " ! "+ str(y[0]) + " ! " + str(y[1]) + " ! " + str(y[2]) + " ! " + str(y[3]) + " ! " +str(y[4]) +" ! " + str(y[5]) +" ! " + "\n"
        arq.write(string)
        
        
    arq.close()
#while true para incio do banco onde mostra todas as funcoes e quando escolhido qualquer uma delas ira ser redirecionado para tal (1=novo cliente/ 2=apaga cliente/3=listar clientes/4=debito/5=deposito/6=extrato/7=transferencia entre contas/8=Poupanca/9=sair)
while True:
    print("1. Novo Cliente")
    print("2. Apaga Cliente")
    print("3. Listar Clientes")
    print("4. Débito")
    print("5. Deposito")
    print("6. Extrato")
    print("7. Transferência entre contas")
    print("8. Poupança")
    print("9.  Sair")
    n=int(input("Digite um número para escolher a sua opção: "))
    #quando digitado o numero 9 o programa ira fechar 
    if n == 9:
        sair()
        break
    elif n == 1:
            novo()
    elif n == 2:
            apaga()
    elif n == 3:
            listar()
    elif n == 4:
            deb()
    elif n == 5:
            dep()
    elif n == 6:
            ext()
    elif n == 7:
            transfentrecontas()
    elif n == 8:
            invest()
    elif n>=10 or n<=10:
            print("Numero Invalido")
