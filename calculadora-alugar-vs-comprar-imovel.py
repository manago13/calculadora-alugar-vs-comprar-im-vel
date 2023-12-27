def valorizacao_imovel(valor_imovel, taxa_valorizacao_imovel_ao_ano, anos):
    meses = anos*12
    taxa_valorizacao_imovel_ao_mes = (1+(taxa_valorizacao_imovel_ao_ano/100))**(1/12)-1
    valor_imovel_acumulado = valor_imovel

    valor_imovel_acumulado_lista = []

    for mes in range (1, meses+1):
      valor_imovel_acumulado *= (1 + taxa_valorizacao_imovel_ao_mes)
      valor_imovel_acumulado_lista.append(valor_imovel_acumulado)
    return valor_imovel_acumulado_lista
    #retorna uma lista em que cada valor se refere ao valor do imóvel já valorizado naquele momento
    #index 0 = valor do imóvel no mês 1. index 1 = valor do imóvel no mês 2

def aplicacao(valor_imovel, taxa_aplicacao_ao_ano, gasto_mensal_aluguel_lista, anos):
    meses = anos*12
    taxa_aplicacao_ao_mes = (1+(taxa_aplicacao_ao_ano/100))**(1/12)-1
    valor_atual_aplicacao = valor_imovel
    valor_atual_aplicacao_lista = []
    rendimento_mensal_lista = []

    for mes in range (1, meses+1):
      rendimento = valor_atual_aplicacao*taxa_aplicacao_ao_mes
      rendimento_mensal_lista.append(rendimento)

      valor_atual_aplicacao *= (1 + taxa_aplicacao_ao_mes)
      valor_atual_aplicacao -= gasto_mensal_aluguel_lista[mes-1]
      valor_atual_aplicacao_lista.append(valor_atual_aplicacao)

    valor_final_aplicado = valor_atual_aplicacao_lista[meses-1]
    return rendimento_mensal_lista, valor_final_aplicado


def gasto_aluguel(valor_aluguel_mensal, taxa_reajuste_aluguel_ao_ano, anos):
    meses = anos*12
    gasto_mensal_aluguel_lista = []
    for mes in range (1, meses+1):
      if (mes-1)%12==0 and (mes-1)!=0: #o valor será reajustado sempre num mês multiplo de 12 + 1
          valor_aluguel_mensal *= (1 + (taxa_reajuste_aluguel_ao_ano/100))
      gasto_mensal_aluguel_lista.append(valor_aluguel_mensal)

    return gasto_mensal_aluguel_lista
    #retorna uma lista em que cada valor se refere ao gasto acumulado até aquele momento.
    #index 0 = acumulado até o mês 1. index 1 = acumulado até o mês 2

valor_imovel = float(input("Informe o valor total do imóvel "))
taxa_valorizacao_imovel_ao_ano = float(input("Qual a taxa anual de valorização do imóvel (em %)? "))
juros_aplicacao_ao_ano = float(input("Qual a taxa anual de rentabilidade da aplicação (em %)? "))
valor_aluguel_mes = float(input("Informe o valor inicial do aluguel "))
taxa_reajuste_aluguel_ao_ano = float(input("Qual a taxa anual de reajuste do aluguel (em %)? "))
anos = int(input("Por quantos anos você pretende alugar e investir seu dinheiro? "))


valor_total_do_imovel_por_mes = valorizacao_imovel(valor_imovel, taxa_valorizacao_imovel_ao_ano, anos)
gasto_mensal_aluguel = gasto_aluguel(valor_aluguel_mes, taxa_reajuste_aluguel_ao_ano, anos)
valor_mensal_rendimento = aplicacao(valor_imovel, juros_aplicacao_ao_ano, gasto_mensal_aluguel, anos)[0]


valor_final_do_imovel = valor_total_do_imovel_por_mes[anos*12-1]
valor_final_aplicado = aplicacao(valor_imovel, juros_aplicacao_ao_ano, gasto_mensal_aluguel, anos)[1]
gasto_total_aluguel = sum(gasto_mensal_aluguel)

print('-------------------------------------------------')

print('Ao final de {} anos, você terá:'.format(anos))

print('Valor gasto com aluguel: R${}'.format('%.2f'%gasto_total_aluguel))
print('Valor acumulado de aplicação: R${}'.format('%.2f'%valor_final_aplicado))
print('Valor do imóvel valorizado: R${}'.format('%.2f'%valor_final_do_imovel))

print('\n')
print('-------------------------------------------------')

def verificacao_turnover(gasto_mensal_aluguel, valor_mensal_rendimento):
    lista = []
    situacao = 'alugar'
    mes_turnover = 0

    # Verificação do mês em que o rendimento não cobre mais o aluguel
    for i in range(len(gasto_mensal_aluguel)):
        if gasto_mensal_aluguel[i] > valor_mensal_rendimento[i]:
            mes = i + 1
            if situacao == 'alugar':
              mes_turnover = mes
            situacao = 'comprar'
        else:
            situacao = 'alugar'
    if mes_turnover != 0:
      print('A partir do {}º mês houve turnover: os rendimentos mensais não cobrirão mais o valor do aluguel.'.format(mes_turnover))
    else:
      print('Os valores dos rendimentos mensais sempre cobrirão os valores gastos com aluguel')

    # Validação final se vale ou não comprar o imóvel (se o valor do imóvel é maior ou menor do que a aplicação menos o aluguel)
    if valor_final_do_imovel > valor_final_aplicado:
      print('A partir das informações dadas acima, será melhor comprar o imóvel ao invés de alugá-lo.')
    else:
      print('A partir das informações dadas acima, será melhor alugar o imóvel e investir o seu valor em aplicação.')
    return