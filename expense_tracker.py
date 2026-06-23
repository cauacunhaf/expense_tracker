import csv

class Despesa:
    def __init__(self, descricao, valor, mes, categoria):
        self.descricao = descricao
        self.valor = valor 
        self.mes = mes
        self.categoria = categoria 

    @property
    def descricao(self):
        return self.__descricao
    
    @descricao.setter
    def descricao(self, nova_descricao):
        if not nova_descricao:
            raise ValueError(
                "A descrição não pode ficar vazia!"
            )
        if nova_descricao.isdigit():
            raise ValueError(
                "A descrição não pode conter apenas números!"
            )
        self.__descricao = nova_descricao
    
    @property
    def valor(self):
        return self.__valor
    
    @valor.setter
    def valor(self, novo_valor):
        if novo_valor <= 0:
            raise ValueError(
                "O valor deve ser maior que zero!"
            )
        self.__valor = novo_valor

    @property
    def mes(self):
        return self.__mes
    
    @mes.setter
    def mes(self, novo_mes):
        if novo_mes < 1 or novo_mes > 12:
            raise ValueError(
                "Digite um mês entre 1 e 12!"
            )
        self.__mes = novo_mes

    @property
    def categoria(self):
        return self.__categoria
    
    @categoria.setter
    def categoria(self, nova_categoria):
        if not nova_categoria:
            raise ValueError(
                "A categoria não pode ficar vazia!"
            )
        if nova_categoria.isdigit():
            raise ValueError(
                "A categoria não pode conter apenas números!"
            )
        self.__categoria = nova_categoria

class ControleDespesas:
    def __init__(self):
        self.__despesas = []
        self.__orcamentos = {}
    
    def inserir(self):
    
        try:
            descricao = input("Digite a descrição da despesa: ").strip().lower()
            categoria = input("Digite a categoria da despesa: ").strip().lower()
            valor = float(input("Digite o valor da despesa: "))
            mes = int(input("Digite o mês da despesa (1-12): "))

            self.__despesas.append(
                Despesa(descricao, valor, mes, categoria)
            )

            print("Despesa cadastrada com sucesso!")

            self.verificar_orcamento(mes)

        except ValueError as erro:
            print(erro)

    def atualizar(self):
        if not self.__despesas:
            print("A lista está vazia!")
            return 
        
        descricao = input("Digite o nome da descrição que deseja atualizar: ").strip().lower()

        try:
            mes = int(input("Digite o mês da despesa: "))
        except ValueError:
            print("Digite apenas números!")
            return

        despesa = self.buscar_despesa(descricao, mes)

        if despesa is None:
            print("Despesa não encontrada!")
            return

        try:
            novo_valor = float(input("Digite o novo valor: "))
            despesa.valor = novo_valor
            print("Valor alterado com sucesso!")
            
            self.verificar_orcamento(despesa.mes)

        except ValueError as erro:
            print(erro)
        

    def excluir(self):
        if not self.__despesas:
            print("A lista está vazia!")
            return
        
        descricao = input("Digite o nome da descrição que deseja excluir: ").strip().lower()
        try:
            mes = int(input("Digite o mês da despesa: "))
        except ValueError:
            print("Digite apenas números!")
            return

        despesa = self.buscar_despesa(descricao, mes)

        if despesa is None:
            print("Despesa não encontrada!")
            return
        
        self.__despesas.remove(despesa)

        print("Despesa excluída com sucesso!")

        self.verificar_orcamento(despesa.mes)


    def buscar_despesa(self, descricao, mes):
        
        for despesa in self.__despesas:
            if (
                despesa.descricao == descricao 
                and despesa.mes == mes
                ):
                return despesa
            
        return None
    
    def listar_despesas(self):

        for indice, despesa in enumerate(self.__despesas, start = 1):
            print(
                f"{indice} - "
                f"{despesa.descricao} - "
                f"R$ {despesa.valor} - "
                f"Mês: {despesa.mes} - "
                f"Categoria: {despesa.categoria}"
            )
    
    def visualizar(self):

        if not self.__despesas:
            print("A lista está vazia!")
            return
        
        self.listar_despesas()
        total = self.calcular_total()
        print(f"\nTotal gasto: R$ {total:.2f}")

    def calcular_total(self):
        return sum(
            despesa.valor
            for despesa in self.__despesas
        )
    
    def resumo_mes(self):

        if not self.__despesas:
            print("A lista está vazia!")
            return
        
        
        try:
            mes = int(input("Digite o mês que deseja consultar (1-12): "))

        except ValueError:
            print("Digite apenas números!")
            return

        total_mes = 0
        encontrou = False

        print(f"\nDespesas do mês {mes}:\n")

        for despesa in self.__despesas:
            if despesa.mes == mes:
                print(
                    f"{despesa.descricao} - "
                    f"R$ {despesa.valor:.2f} - "
                    f"{despesa.categoria}"
                )

                total_mes += despesa.valor
                encontrou = True

        if encontrou:
            print(f"\nTotal do mês: R$ {total_mes:.2f}")
            self.verificar_orcamento(mes)
        else:
            print("Não existem despesas cadastradas para esse mês.")

    def filtrar_categoria(self):

        if not self.__despesas:
            print("A lista está vazia!")
            return
        
        categoria = input("Digite a categoria: ").strip().lower()

        encontrou = False

        for despesa in self.__despesas:
            if despesa.categoria == categoria:
                print(
                    f"{despesa.categoria} - "
                    f"R$ {despesa.valor:.2f} - "
                    f"Mês {despesa.mes}"
                )
                encontrou = True
        
        if not encontrou:
            print("Nenhuma despesa encontrada nessa categoria")
    
    def definir_orcamento(self):

        try:
            mes = int(input("Digite o mês: "))
            valor = float(input("Digite o orçamento: "))

            self.__orcamentos[mes] = valor

            print("Orçamento cadastrado!")
        
        except ValueError:
            print("Digite valores válidos!")

    def verificar_orcamento(self, mes):

        total_mes = sum(
            despesa.valor
            for despesa in self.__despesas
            if despesa.mes == mes
        )

        orcamento = self.__orcamentos.get(mes)

        if (
            orcamento is not None 
            and total_mes > orcamento
        ):
            print(
                f"⚠ Orçamento excedido em "
                f"R$ {total_mes - orcamento:.2f}"
            )

    def exportar_csv(self):

        with open(
            "despesas.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as arquivo:
            
            writer = csv.writer(arquivo)
            
            writer.writerow(
                ["descriçao", "valor", "mes", "categoria"]
            )

            for despesa in self.__despesas:
                writer.writerow(
                    [
                        despesa.descricao,
                        despesa.valor,
                        despesa.mes,
                        despesa.categoria
                    ]
                )
        
        print("Arquivo exportado com sucesso!")

    
controle = ControleDespesas()

while True:
    print(
        "- [i] inserir\n" \
        "- [a] atualiza\n" \
        "- [e] excluir\n" \
        "- [v] visualizar\n" \
        "- [r] resumir mês\n" \
        "- [f] filtrar categoria\n"
        "- [d] definir orçamento\n"
        "- [c] exportar arquivo\n"\
        "- [s] sair"
    )
    letra = input("Escolha uma das opções: ").strip().lower()

    if letra == "i":
        controle.inserir()
    
    elif letra == "a":
        controle.atualizar()

    elif letra == "e":
        controle.excluir()
    
    elif letra == "v":
        controle.visualizar()

    elif letra == "r":
        controle.resumo_mes()

    elif letra == "f":
        controle.filtrar_categoria()

    elif letra == "d":
        controle.definir_orcamento()

    elif letra == "c":
        controle.exportar_csv()
    
    elif letra == "s":
        print("Programa encerrado!")
        break

    else: 
        print("Digite apenas 'i', 'a', 'e', 'v', 'r', 'f', 'd', 'c' ou 's'")


        