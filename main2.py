import random
import string
from dataclasses import dataclass
from typing import List

TARGET = "Hola Mundo!"
POPULATION_SIZE = 200
MUTATION_RATE = 0.02
MAX_GENERATIONS = 10000

GENES = string.ascii_letters + string.digits + " .,!?¡¿"

@dataclass
class Individual:
    chromosome: str
    fitness: int

    @classmethod
    def random(cls):
        chromosome = "".join(
            random.choice(GENES)
            for _ in range(len(TARGET))
        )
        return cls(chromosome, cls.calculate_fitness(chromosome))

    @staticmethod
    def calculate_fitness(chromosome: str) -> int:
        return sum(
            1
            for a, b in zip(chromosome, TARGET)
            if a == b
        )

    def crossover(self, other):
        child = []

        for a, b in zip(self.chromosome, other.chromosome):

            r = random.random()

            if r < 0.45:
                child.append(a)
            elif r < 0.90:
                child.append(b)
            else:
                child.append(random.choice(GENES))

        child = "".join(child)

        return Individual(
            child,
            Individual.calculate_fitness(child)
        )

    def mutate(self):

        chars = list(self.chromosome)

        for i in range(len(chars)):

            if random.random() < MUTATION_RATE:
                chars[i] = random.choice(GENES)

        self.chromosome = "".join(chars)
        self.fitness = Individual.calculate_fitness(self.chromosome)

population: List[Individual] = [
    Individual.random()
    for _ in range(POPULATION_SIZE)
]

generation = 0

while generation < MAX_GENERATIONS:

    population.sort(
        key=lambda x: x.fitness,
        reverse=True
    )

    best = population[0]

    print(
        f"Generación {generation:5d} | "
        f"Fitness {best.fitness:2d}/{len(TARGET)} | "
        f"{best.chromosome}"
    )

    if best.fitness == len(TARGET):
        print("\n¡Objetivo encontrado!")
        break

    new_population = []

    elite = population[:POPULATION_SIZE // 10]

    new_population.extend(elite)

    while len(new_population) < POPULATION_SIZE:

        parent1 = random.choice(population[:50])
        parent2 = random.choice(population[:50])

        child = parent1.crossover(parent2)
        child.mutate()

        new_population.append(child)

    population = new_population

    generation += 1

else:
    print("\nNo se encontró una solución.")
