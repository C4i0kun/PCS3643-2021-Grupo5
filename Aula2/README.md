# Aula 2 - Especificação de Casos de Uso

## 📊 Diagrama de Casos de Uso

![image info](./diagrama_casos_de_uso.png)

## Especificação dos Casos de Uso

### Ofertar Lotes de Produtos

**Nome**: Ofertar lotes de produtos.

**Descrição**: Este caso de uso permite ao leiloeiro o cadastramento de um lote de um ou mais produtos de um vendedor e define seus preços mínimos.

**Ator(es)**: Vendedor, Leiloeiro

**Evento Iniciador**: Vendedor solicita a criação de um novo lote de produtos.

**Pré-condições**:

- Vendedor cadastrado

**Sequência de Eventos**:

1. Vendedor solicita a criação de um novo lote de produtos.
2. O vendedor entra com dados dos produtos que deseja ofertar no lote, explicitando características como nome, quantidade, preço, etc.
3. O sistema envia uma mensagem de confirmação ao vendedor.
4. O vendedor confirma a criação do lote de de produtos.
5. O leiloeiro cadastra o lote com o valor mínimo de lance, o período do leilão.
6. Vendedor paga a taxa de comissão ao site.
7. Leiloeiro registra o pagamento da taxa e confirma a oferta do lote.
8. Sistema adiciona o lote no catálogo.
9. Fim do caso de uso.

**Pós-condições**: 

- Lote de produtos gerado com sucesso.

**Fluxos alternativos**: 

- No passo 3, o vendedor pode cancelar a sequência de eventos, finalizando o caso de uso sem criar um lote de produtos.
- No passo 4, caso o vendedor não confirme a criação do lote de produtos, ele pode retorna ao passo 2 para editá-los e/ou cancelar a sequência de eventos.
- No passo 6, caso o vendedor não pague a taxa de comissão, o leiloeiro pode cancelar a oferta do lote e encerra o caso de uso.

**Exceções**:

- No passo 4, caso seja confirmada a criação de um lote sem produtos, o sistema exibe uma mensagem de erro e o caso de uso se encerra.

### Realizar Leilão

**Nome**: Realizar Leilão.

**Descrição**: Este caso de uso engloba todas as ações dos atores durante o Leilão. O Leiloeiro inicializa um leilão, e a partir disso os atores podem monitorar os lances do leilão até que o leiloeiro o finalize definindo o lance vencedor.

**Evento Iniciador**: Leiloeiro solicita a inicialização de um Leilão.

**Atores**:

 - Leiloeiro
 - Comprador
 - Vendedor

**Pré-condições**: 

- Leiloeiro, compradores e vendedores autenticados.
- Lotes cadastrados disponíveis no sistema.

**Sequência de Eventos**:

1. Leiloeiro solicita a inicialização de um Leilão.
2. Sistema checa se existem lotes cadastrados disponíveis no sistema.
3. Leiloeiro adiciona o lote desejado ao leilão.
4. Leiloeiro finaliza a criação do Leilão.
5. Sistema inicia o Leilão.
6. Compradores fazem seus lances nos lotes.
7. Sistema verifica se o lance é válido.
8. Sistema atualiza o candidato ao lote com base nos novos lances.
9. Sistema verifica o fim do leilão.
10. Sistema define o lance vencedor para o lote.
11. Sistema verifica se o lance vencedor supera o valor mínimo do lote.
12. Sistema finaliza o leilão.
13. Comprador paga o valor do seu lance somado a taxa de comissão.
14. Leiloeiro registra o pagamento do lance vencedor no sistema. 
15. Fim de Caso de Uso.

**Pós-Condições**:

 - Leilão finalizado com sucesso

**Fluxos Alternativos**:

 - Entre o passo 5 e o passo 8, o vendedor pode cancelar o leilão a qualquer momento, pagando uma taxa e encerrando o caso de uso.
 - Entre o passo 5 e o passo 8, o leiloeiro, o vendedor e os compradores podem monitorar os lances e o horário de fim do Leilão.
 - Entre o passo 5 e o passo 8, o leiloeiro pode cancelar o leilão a qualquer momento, encerrando o caso de uso.

**Exceções**:

 - No passo 3, caso não existam lotes cadastrados disponíveis no sistema, exibe uma mensagem informando a indisponibilidade de lotes e encerra o caso de uso.

### Gerar Relatórios

**Nome**: Gerar Relatórios.

**Descrição**: Este caso de uso permite ao leiloeiro gerar um relatório de desempenho ou de faturamento contendo várias informações referentes ao leilão que acaba de ser completado.

**Evento Iniciador**: Leiloeiro solicita a geração do relatório.

**Atores**:

 - Leiloeiro

**Pré-condições**: 

- Leiloeiro Autenticado
- Leilão Finalizado com Lote Vendido

**Sequência de Eventos**:

1. Leiloeiro solicita a geração do relatório
2. Leiloeiro informa que deseja obter um relatório de desempenho.
3. Sistema agrega as informações do desempenho do leilão em um documento.
4. Sistema apresenta este documento ao Leiloeiro.
5. Fim de Caso de Uso.

**Pós-Condições**:

 - Documento gerado com sucesso.

**Fluxos Alternativos**:

 - No passo 2, o leiloeiro pode informar que deseja obter um relatório de faturamento, alterando o fluxo para que o sistema agregue as informações para gerar este tipo de relatório.
 - No passo 5, o leiloeiro pode escolher baixar o documento e é desviado para a seção Baixar Relatório.

**Exceções**:

 - No passo 3, caso o sistema não encontre dados suficientes do leilão para gerar um relatório, exibe uma mensagem de erro e encerra o caso de uso.
