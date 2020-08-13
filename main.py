from bingo import BingoGenerator
from loader import JSONLoader

MAX_BINGOS = 12


def main():
    print("Добро пожаловать в генератор бинго научной роты!\n")

    loader = JSONLoader()
    data = loader.load_data()

    print("Доступные бинго:")
    for i, item in enumerate(data):
        print("{}. {} ({} шт.)".format(
            i + 1,
            item.title,
            len(item.phrases)
        ))

    try:
        bingo = int(input("Введите номер бинго ")) - 1
        current_bingo = data[bingo]

        amount = int(input("Введите количество бинго для генерации "))
        if amount <= 0 or amount > MAX_BINGOS:
            raise KeyError

        new_bingo = BingoGenerator(
            current_bingo
        )

        for _ in range(amount):
            new_bingo.generate_bingo()
            print("Готово!")

    except ValueError:
        print("Введите целочисленное значение!")
        return

    except IndexError:
        print("Такого номера бинго нет!")
        return

    except KeyError:
        print("Некорректное число бинго для генерации!")
        print("Могу сгенерировать максимум {} бинго".format(
            MAX_BINGOS
        ))
        return

    except KeyboardInterrupt:
        print("Работы программы завершена!")

    finally:
        input("Нажмите ENTER для продолжения...")


if __name__ == "__main__":
    main()
