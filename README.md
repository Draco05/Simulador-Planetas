# Simulador-Planetas
## Descrição
Esse projeto é uma simulação da interação entre corpos celestes de mesma massa por meio da ação da força gravitacional. O principal objetivo desse projeto é conseguir simular situações em que existem mais de 2 planetas, pois isso não tem uma solução geral matemática e facilmente torna-se um sistema caótico. O usuário controla o estado do incial sistema, adicionando planetas e ativando ou não se as colisões serão consideradas, além de conseguir obter informações da posição e da velocidade de cada planeta. Por questões de simplicidade, foi utilizado a massa e o raio do sol como referência dos dados do planeta.

https://github.com/user-attachments/assets/55ca2644-7c21-4b65-b003-b3f36405d0ec

## Controles
Movimentar a visão: setas do teclado

Zoom-in: tecla i

Zoom-out: tecla o

Adicionar planeta: botão esquerdo do mouse em qualquer lugar na tela

## A física na simulação
Para iniciar a modelagem, foi considerado o sistema de coordeandas de base ortonormal com as componentes $\hat{i}$ e $\hat{j}$. Inicialmente a tela está no quarto quadrante, mas isso não afeta o resto da modelagem.

Para calcular a força resultante de cada planeta $i$, foi utilizado a expressão $\vec{F_i} = \sum_{j=1}^{n} \vec{F_{gij}}$, sendo $\vec{F_{gij}}$ a força gravitacional entre os planetas $i$ e $j$. No caso em que $i = j$, essa força é nula.
O módulo da força gravitacional é calculada por meio da expressão: 

$$\begin{align} F_{gij} = \frac{m_i \cdot m_j \cdot G}{||{ \vec{r_j} - \vec{r_i}}||^2}.\end{align}$$
       
Esse módulo da força gravitacional é utilizado para calcular a força para cada componente do sistema de coordenadas, ficando então a expressão:

$$ \begin{align} \vec{F_{gij}} = F_{gij} \frac{(x_j - x_i)}{||{ \vec{r_j} - \vec{r_i}}||^2} \hat{i} + F_{gij} \frac{(y_j - y_i)}{||{ \vec{r_j} - \vec{r_i}}||^2} \hat{j}. \end{align}$$

Assim, com as forças resultantes de cada planeta, é calculado a aceleração por meio da Segunda Lei de Newton: $\vec{a_i} = \frac{1}{m_i} \vec{F_i}.$ Essa aceleração é utilizada para aproximar a nova velocidade, em que o Método de Euler foi utilizado nesse processo. Essa aproximação é dada por $\vec{v_{t+dt}} = \vec{v_t} + dt \cdot \vec{a_t}$, em que a velocidade em $t+dt$ é o valor aproximado dela, $t$ é o valor imediantamente passado dela e $dt$ é a variação do tempo. Um valor de $dt$ pequeno consegue produzir um resultado mais preciso da simulação, porém com um custo alto de computação. Por essa razão, foi determinado no programa que $dt = 3600s = 1 h$, que, para um sistema celestial, serve como uma aproximação boa. 

Esse Método de Euler também é utilizado para aproximar a nova posição do corpo, ficando então a expressão $\vec{r_{t+dt}} = \vec{r_t} + dt \cdot \vec{v_t}$.

Realizando esse processo repetidamente para todos os planetas, conseguimos aproximar como esse sistema de planetas se comporta, porém, por ser simplesmente uma simulação, há uma margem de erro a ser considerada.


## Detecção de Colisões
O programa permite ativar ou desativar a colisão entre planetas. Com a opção ativada, a colisão ocorre quando a distância entre dois planetas é menor ou igual a soma dos seus raios. Esse é o mesmo processo utilizado para considerar se existe uma intersecção entre dois círculos. Se houver colisão, o programa é pausado, pois seria necessário um estudo mais aprofundado do que realmente aconteceria nesses casos. Com a opção desativada, o sistema torna-se menos realista, porém muito mais caótico, o que é visualmente interessante. 

## Como executar o código
É necessário ter pelo menos o Python 3.10 instalado no computador para que o código seja executado. Caso não tenha, entre [aqui](https://www.python.org/downloads/) para baixá-lo e instalá-lo.
Caso não possua a biblioteca PyGame instalada, execute este comando no terminal:
```
pip install pygame
```
Por fim, para executar o código clone esse repositório no seu computador, por meio do comando:
```
git clone https://github.com/Draco05/Simulador-Planetas
```
E rode localmente usando o comando:
```
python projeto.py
```

## Participantes do Projeto
Caio Draco Araújo Albuquerquer Galvão;

João Pedro Boiago Gomes Santana;

Luis Guilherme Zanetti;

Pedro Henrique Barbosa Oliveira.


## Referências
BERNARDES, Esmerindo. Dinâmica-v4(Notas de Aula). IFSC: Universidade de São Paulo, 2024.

BERNARDES, Esmerindo. Gravitação (Notas de Aula). IFSC: Universidade de São Paulo, 2024.

https://pt.wikipedia.org/wiki/M%C3%A9todo_de_Euler

https://en.wikipedia.org/wiki/Three-body_problem



