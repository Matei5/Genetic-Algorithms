import random
import math

def decode(cromozom, biti, x_min, x_max):
    interval = x_max - x_min
    scala = (1 << biti) - 1
    return x_min + cromozom * interval / scala

def f(x, a, b, c):
    return a * x * x + b * x + c

def format_x(valoare):
    return f"{valoare:9.6f}"

with open("input.txt") as fin:
    dimensiune_populatie = int(fin.readline())  # dimensiune populatie
    x_min, x_max = map(float, fin.readline().split())
    A, B, C = map(float, fin.readline().split())  # coeficienti functie
    precizie = int(fin.readline())  # precizie
    prob_recombinare = float(fin.readline())  # probabilitate recombinare
    prob_mutatie = float(fin.readline())  # probabilitate mutatie
    nr_generatii = int(fin.readline())  # numar generatii

biti = math.ceil(math.log2((x_max - x_min) * (10**precizie) + 1))
populatie = [random.randint(0, (2**biti) - 1) for _ in range(dimensiune_populatie)]
istoric_maxim = []

with open("Evolutie.txt", "w") as fout:
    for generatie in range(nr_generatii):
        decodificat = [decode(cromozom, biti, x_min, x_max) for cromozom in populatie]
        fitness = [f(x, A, B, C) for x in decodificat]
        fitness_total = sum(fitness) 
        fitness_maxim = max(fitness)
        istoric_maxim.append(fitness_maxim)

        if generatie == 0:
            fout.write("Populatia initiala\n")
            for i, cromozom in enumerate(populatie):
                binar = bin(cromozom)[2:].rjust(biti, '0')
                x_str = format_x(decodificat[i])
                fout.write(f"  {i+1:2d}: {binar} x= {x_str} f={fitness[i]}\n")

            fout.write("\nProbabilitati selectie \n")
            probabilitati = [fit / fitness_total for fit in fitness]
            for i, prob in enumerate(probabilitati):
                fout.write(f"cromozom {i+1:4d} probabilitate {prob}\n")

            fout.write("\nIntervale probabilitati selectie \n")
            cumulative = [0.0]
            for p_i in probabilitati:
                cumulative.append(cumulative[-1] + p_i)
            for valoare in cumulative:
                fout.write(str(valoare) + " ")
            fout.write("\n")

            fout.write("")
            populatie_noua = []
            for _ in range(dimensiune_populatie):
                u = random.random()
                stanga, dreapta = 0, dimensiune_populatie
                while dreapta - stanga > 1:
                    mijloc = (stanga + dreapta) // 2
                    if cumulative[mijloc] > u:
                        dreapta = mijloc
                    else:
                        stanga = mijloc
                fout.write(f"u={u}  selectam cromozomul {dreapta}\n")
                populatie_noua.append(populatie[dreapta - 1])

            fout.write("\nDupa selectie:\n")
            decodificat_selectie = [decode(cromozom, biti, x_min, x_max) for cromozom in populatie_noua]
            fitness_selectie = [f(x, A, B, C) for x in decodificat_selectie]
            for i, cromozom in enumerate(populatie_noua):
                binar = bin(cromozom)[2:].rjust(biti, '0')
                x_str = format_x(decodificat_selectie[i])
                fout.write(f"  {i+1:2d}: {binar} x= {x_str} f={fitness_selectie[i]}\n")

            fout.write(f"\nProbabilitatea de recombinare {prob_recombinare}\n")
            for i, cromozom in enumerate(populatie_noua):
                u = random.random()
                binar = bin(cromozom)[2:].rjust(biti, '0')
                fout.write(f"{i+1}: {binar} u={u}")
                fout.write("<" + str(prob_recombinare) + " participa \n" if u < prob_recombinare else "\n")
            fout.write("")

        else:
            fout.write(f"\nGeneratia {generatie+1}: Max Fitness={fitness_maxim} Mean Fitness={fitness_total/dimensiune_populatie}")

        # Selectie, recombinare, mutatie
        probabilitati = [fit / fitness_total for fit in fitness]
        cumulative = [0.0]
        for p_i in probabilitati:
            cumulative.append(cumulative[-1] + p_i)
        populatie_noua = []
        for _ in range(dimensiune_populatie):
            u = random.random()
            stanga, dreapta = 0, dimensiune_populatie
            while dreapta - stanga > 1:
                mijloc = (stanga + dreapta) // 2
                if cumulative[mijloc] > u:
                    dreapta = mijloc
                else:
                    stanga = mijloc
            populatie_noua.append(populatie[dreapta - 1])

        # Recombinare
        de_recombinat = []
        for i in range(dimensiune_populatie):
            if random.random() < prob_recombinare:
                de_recombinat.append(i)
        for i in range(0, len(de_recombinat) - 1, 2):
            idx1 = de_recombinat[i]
            idx2 = de_recombinat[i+1]
            c1 = populatie_noua[idx1]
            c2 = populatie_noua[idx2]
            punct_taiere = random.randint(0, biti - 1)
            masca = (1 << (biti - punct_taiere)) - 1
            c1_nou = ((c1 >> (biti - punct_taiere)) << (biti - punct_taiere)) + (c2 & masca)
            c2_nou = ((c2 >> (biti - punct_taiere)) << (biti - punct_taiere)) + (c1 & masca)
            populatie_noua[idx1] = c1_nou
            populatie_noua[idx2] = c2_nou

        # Mutatie
        for i in range(dimensiune_populatie):
            for pozitie_bit in range(biti):
                if random.random() < prob_mutatie:
                    populatie_noua[i] ^= (1 << pozitie_bit)
        populatie = populatie_noua
