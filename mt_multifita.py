import time

class MaquinaTuringMultifita:
    def __init__(self):
        # B = Branco (Blank)
        # S = Stay, R = Right, L = Left
        self.transicoes = {}
        self.construir_transicoes()

    def construir_transicoes(self):
        alfabeto = ['a', 'b', 'c', 'r', 's', 'l', 'w', 'i']
        
        # 1. q_start: Escreve marcadores de início nas Fitas 2 e 3
        # (Lê T1, T2, T3) -> (Novo Estado, Escreve T1, T2, T3, Move T1, T2, T3)
        for x in alfabeto:
            self.transicoes[('q_start', x, 'B', 'B')] = ('q_copy', x, '[', '[', 'S', 'R', 'R')

        # 2. q_copy: Copia T1 para T2 e T3 simultaneamente
        for x in alfabeto:
            self.transicoes[('q_copy', x, 'B', 'B')] = ('q_copy', x, x, x, 'R', 'R', 'R')
        
        # 3. q_mark1: T1 achou o final da palavra original (B). Escreve '#'
        self.transicoes[('q_copy', 'B', 'B', 'B')] = ('q_rewind_t2', '#', 'B', 'B', 'R', 'L', 'S')

        # 4. q_rewind_t2: Rebobina a Fita 2 até achar o marcador '['
        for x in alfabeto:
            self.transicoes[('q_rewind_t2', 'B', x, 'B')] = ('q_rewind_t2', 'B', x, 'B', 'S', 'L', 'S')
        self.transicoes[('q_rewind_t2', 'B', '[', 'B')] = ('q_concat_w', 'B', '[', 'B', 'S', 'R', 'S')

        # 5. q_concat_w: Escreve o conteúdo da Fita 2 na Fita 1
        for x in alfabeto:
            self.transicoes[('q_concat_w', 'B', x, 'B')] = ('q_concat_w', x, x, 'B', 'R', 'R', 'S')
        
        # 6. q_mark2: Fita 2 terminou. Escreve o segundo '#' na Fita 1 e prepara Fita 3
        self.transicoes[('q_concat_w', 'B', 'B', 'B')] = ('q_concat_rev', '#', 'B', 'B', 'R', 'S', 'L')

        # 7. q_concat_rev: Escreve o conteúdo da Fita 3 na Fita 1 de trás para frente (w^R)
        for x in alfabeto:
            self.transicoes[('q_concat_rev', 'B', 'B', x)] = ('q_concat_rev', x, 'B', x, 'R', 'S', 'L')
        
        # 8. q_accept: Fita 3 achou o marcador '['. Finaliza.
        self.transicoes[('q_concat_rev', 'B', 'B', '[')] = ('q_accept', 'B', 'B', '[', 'S', 'S', 'S')

    def rastrear_execucao(self, palavra):
        # Inicializa as fitas com espaços em branco (100 posições para evitar Index Error)
        t1 = list(palavra) + ['B'] * 50
        t2 = ['B'] * 50
        t3 = ['B'] * 50
        
        # Cabeças de leitura
        c1, c2, c3 = 0, 0, 0
        estado = 'q_start'
        
        print(f"\n{'='*60}")
        print(f"RASTREIO: Máquina de Turing Multifita (3 Fitas)")
        print(f"Objetivo: w -> w#w#w^R | Entrada: {palavra}")
        print(f"{'='*60}")

        passos = 0
        while estado != 'q_accept':
            l1, l2, l3 = t1[c1], t2[c2], t3[c3]
            chave = (estado, l1, l2, l3)
            
            # Print do Rastreio
            if passos % 3 == 0 or chave not in self.transicoes: # Imprime passos relevantes para não poluir
                fita1_str = "".join(t1).replace('B', '').strip()
                print(f"[{estado:<12}] T1: {fita1_str:<12} | C1:{c1} C2:{c2} C3:{c3}")
            passos += 1

            if chave in self.transicoes:
                estado_novo, e1, e2, e3, m1, m2, m3 = self.transicoes[chave]
                
                # Escreve nas fitas
                t1[c1], t2[c2], t3[c3] = e1, e2, e3
                estado = estado_novo
                
                # Move as cabeças
                if m1 == 'R': c1 += 1
                elif m1 == 'L': c1 -= 1
                
                if m2 == 'R': c2 += 1
                elif m2 == 'L': c2 -= 1
                
                if m3 == 'R': c3 += 1
                elif m3 == 'L': c3 -= 1
            else:
                print("\n[!] Transição Indefinida. Rejeitado ou Crash.")
                break
            
            time.sleep(0.1)

        if estado == 'q_accept':
            resultado_final = "".join(t1).replace('B', '').strip()
            print(f"\n{'-'*60}")
            print(f"RESULTADO: ACEITO")
            print(f"Fita 1 Final: {resultado_final}")
            print(f"{'-'*60}")

# Teste
mt = MaquinaTuringMultifita()
mt.rastrear_execucao("abc") # Deve gerar abc#abc#cba
mt.rastrear_execucao("www")
mt.rastrear_execucao("brasil")