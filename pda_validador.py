import time

class AutomatoPilha:
    def __init__(self):
        # Definição Formal do PDA
        self.estados = {'q0', 'q_var', 'q_num', 'q_op', 'q_open', 'q_close', 'q_accept', 'q_reject'}
        self.estado_inicial = 'q0'
        
        # Função de Transição: (estado_atual, tipo_char) -> (novo_estado, acao_pilha)
        # acao_pilha: 'push', 'pop', ou 'none'
        self.transicoes = {
            # Início e após abrir parêntese
            ('q0', 'VAR'): ('q_var', 'none'),
            ('q0', 'NUM'): ('q_num', 'none'),
            ('q0', '('): ('q_open', 'push'),
            ('q_open', 'VAR'): ('q_var', 'none'),
            ('q_open', 'NUM'): ('q_num', 'none'),
            ('q_open', '('): ('q_open', 'push'),
            
            # Após ler variável ou número (espera operador ou fechar parêntese)
            ('q_var', 'OP'): ('q_op', 'none'),
            ('q_var', ')'): ('q_close', 'pop'),
            ('q_var', 'EOF'): ('q_accept', 'none'), # Fim da expressão
            
            ('q_num', 'OP'): ('q_op', 'none'),
            ('q_num', ')'): ('q_close', 'pop'),
            ('q_num', 'EOF'): ('q_accept', 'none'),
            
            # Após ler operador (espera variável, número ou abrir parêntese)
            ('q_op', 'VAR'): ('q_var', 'none'),
            ('q_op', 'NUM'): ('q_num', 'none'),
            ('q_op', '('): ('q_open', 'push'),
            
            # Após fechar parêntese (espera operador, fechar outro, ou fim)
            ('q_close', 'OP'): ('q_op', 'none'),
            ('q_close', ')'): ('q_close', 'pop'),
            ('q_close', 'EOF'): ('q_accept', 'none'),
        }

    def classificar_char(self, char):
        if char.isalpha(): return 'VAR'
        if char.isdigit(): return 'NUM'
        if char in '+-*/': return 'OP'
        if char in '()': return char
        return 'INV' # Inválido

    def rastrear_execucao(self, expressao):
        estado_atual = self.estado_inicial
        pilha = ['$'] # Símbolo inicial da pilha
        fita_entrada = list(expressao) + ['EOF']
        
        print(f"\n{'='*50}")
        print(f"RASTREIO DE EXECUÇÃO: Autômato de Pilha")
        print(f"Expressão: {expressao}")
        print(f"{'='*50}")
        print(f"{'Estado':<10} | {'Lendo':<7} | {'Ação Pilha':<12} | {'Pilha Atual'}")
        print(f"{'-'*50}")

        for char in fita_entrada:
            tipo_char = 'EOF' if char == 'EOF' else self.classificar_char(char)
            
            # Imprime o passo atual antes da transição
            print(f"{estado_atual:<10} | {char:<7} | ", end="")

            chave = (estado_atual, tipo_char)
            
            if chave in self.transicoes:
                novo_estado, acao = self.transicoes[chave]
                
                # Executa ação na pilha
                if acao == 'push':
                    pilha.append('X')
                    print(f"{'Empilha (X)':<12} | {''.join(pilha)}")
                elif acao == 'pop':
                    if pilha[-1] == '$':
                        print(f"{'Erro (Vazia)':<12} | {''.join(pilha)}")
                        print(f"{'-'*50}\nRESULTADO: REJEITADO (Parênteses desbalanceados)")
                        return False
                    pilha.pop()
                    print(f"{'Desempilha':<12} | {''.join(pilha)}")
                else:
                    print(f"{'Nenhuma':<12} | {''.join(pilha)}")
                
                estado_atual = novo_estado
            else:
                print(f"{'Erro Sintaxe':<12} | {''.join(pilha)}")
                print(f"{'-'*50}\nRESULTADO: REJEITADO (Transição não definida)")
                return False
            time.sleep(0.3) # Efeito visual no terminal

        # Verifica aceitação final
        if estado_atual == 'q_accept' and pilha == ['$']:
            print(f"{'-'*50}\nRESULTADO: ACEITO (Expressão Sintaticamente Correta!)")
            return True
        else:
            print(f"{'-'*50}\nRESULTADO: REJEITADO (Pilha não vazia no final)")
            return False

# Testes da equipe
pda = AutomatoPilha()
pda.rastrear_execucao("(a+b)*c") # Caso de Sucesso
pda.rastrear_execucao("a+*b")    # Falha: Operador duplo
pda.rastrear_execucao("((a+b)")  # Falha: Pilha não vazia