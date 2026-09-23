# Software/Hardware - Fisioterapeuta Digital para Astronautas

## Software

### Nome/ideia central
Fisioterapeuta digital para astronautas: exercício certo, mesmo sem gravidade.

### Objetivo do sistema
Criar um software de monitoramento de saúde para astronautas em missões espaciais, focado em acompanhar exercícios físicos em microgravidade e dar feedback imediato sobre a postura e os ângulos do movimento.

### Funcionamento geral
O sistema usa vídeo do astronauta durante o exercício, estima a pose corporal, calcula ângulos articulares, compara esses ângulos com zonas seguras definidas por protocolo médico e fornece feedback visual imediato.

Fluxo proposto:

1. **Câmeras da estação**
   - Capturam vídeo do astronauta durante o exercício.

2. **Estimativa de pose**
   - Utiliza MediaPipe Pose.
   - Detecta 33 pontos-chave do esqueleto em imagem ou vídeo.

3. **Cálculo de ângulos**
   - Calcula ângulos entre articulações.
   - Exemplos citados:
     - ombro-cotovelo-pulso;
     - quadril-joelho-tornozelo.

4. **Zonas seguras**
   - Compara os ângulos medidos com limites definidos por protocolo médico.
   - Cada exercício possui uma faixa segura de movimento.

5. **Feedback imediato**
   - O feedback pode aparecer em uma tela ou em óculos de realidade aumentada.
   - Quando uma articulação sai da zona segura, a junta fica vermelha.
   - O sistema indica o ajuste postural necessário.

### Exemplo de uso
No exemplo apresentado, o sistema mede o ângulo do joelho durante o exercício.

- Antes do exercício, o protocolo médico define a zona segura do movimento.
- Durante o exercício, o sistema mede o ângulo a cada frame.
- Quando o movimento sai da zona segura, por exemplo com coluna curvada ou sobrecarga na patela, a articulação é marcada em vermelho e o ajuste postural é indicado.

### Banco de dados
O projeto propõe o uso de um banco relacional PostgreSQL para registrar os dados das sessões.

Modelo de dados proposto para o protótipo:

#### Tabela `astronauta`
- `id`
- `nome`

#### Tabela `exercicio`
- `id`
- `nome`
- `articulacao`
- `angulo_min`
- `angulo_max`

#### Tabela `sessao`
- `id`
- `astronauta_id`
- `exercicio_id`
- `inicio`
- `fim`

#### Tabela `medicao`
- `id`
- `sessao_id`
- `instante`
- `angulo`
- `dentro_da_zona`
- `confianca`

### Relatórios gerados
A partir das medições, o sistema deve gerar relatórios com:

- amplitude de movimento por articulação e por sessão;
- tempo dentro e fora da zona segura;
- desvios e assimetria entre lado esquerdo e direito;
- tendência ao longo da missão para estimar a eficácia da contenção da atrofia;
- confiança da detecção em cada medição.

### Plano de validação do software
O documento propõe validar o sistema medindo:

| O que medir | Métrica | Como medir |
|---|---|---|
| Precisão dos ângulos | Erro angular em graus | Comparar com goniômetro ou marcação manual nos frames |
| Detecção de erros de postura | Sensibilidade e falsos alertas | Gravar movimentos corretos e errados de propósito |
| Rapidez do feedback | Latência em milissegundos | Medir o tempo entre o movimento e o aviso na tela |
| Corpo flutuando | Erro angular em várias orientações | Repetir o teste deitado, invertido ou com a imagem girada |

### Riscos e limitações técnicas
O documento identifica os seguintes riscos e formas de tratamento:

| Risco | Como tratar |
|---|---|
| MediaPipe Pose foi treinado sob gravidade; corpo flutuando ou invertido pode falhar | Testar várias orientações; ajustar ou retreinar |
| Elástico e equipamentos podem ocultar articulações | Usar a confiança de cada ponto; ignorar medições fracas |
| Câmera única limita a profundidade dos ângulos | Avaliar mais de uma câmera e validar contra a referência |
| Falsos alertas ou alertas perdidos | Usar zonas definidas pelo protocolo médico; médico acompanha os relatórios |
| Câmeras registram o astronauta, gerando questões de privacidade e dados médicos | Processamento local, consentimento e acesso restrito |

### Próximos passos do protótipo
Os próximos passos técnicos citados são:

- criar um protótipo com MediaPipe Pose, webcam e cálculo de ângulos em um exercício, como agachamento ou remada;
- definir zonas seguras de exemplo;
- implementar feedback visual com junta em vermelho;
- gravar as medições em PostgreSQL;
- gerar um relatório simples;
- medir as métricas do plano de validação;
- procurar dados abertos da NASA que possam ser usados no protótipo.

## Hardware

### Hardware da demo
O documento apresenta três opções de hardware para rodar a demonstração e gravar os dados do projeto.

### Opção 1: TV box
Itens:

- TV box: R$ 100,00
- Cabo plug P4: R$ 26,00
- SanDisk Extreme 64 GB: R$ 214,99
- 2 mini tripés de mesa: incluídos no total

Total com os tripés: **R$ 385,97**

### Opção 2: Raspberry Pi 5 (4 GB)
Itens:

- Raspberry Pi 5 4 GB: R$ 1.294,00
- Fonte oficial 27 W: R$ 123,31
- Case com cooler: R$ 89,96
- Cabo micro-HDMI: R$ 28,40
- SanDisk Extreme 64 GB: R$ 214,99
- 2 mini tripés de mesa: incluídos no total

Total com os tripés: **R$ 1.795,64**

### Opção 3: Mini PC Intel Celeron
Itens:

- Mini PC Celeron: R$ 600,00
- 2 mini tripés de mesa: incluídos no total

Total com os tripés: **R$ 644,98**

### Itens comuns às três opções
- 2 mini tripés de mesa: R$ 44,98, já incluídos nos totais.
- Webcam: valor ainda a definir, fora dos totais.

### Uso previsto do hardware
O hardware será usado para:

- rodar a demonstração;
- capturar ou processar o vídeo do exercício;
- executar o protótipo;
- gravar os dados do projeto.
