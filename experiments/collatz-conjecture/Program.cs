using System;
using System.Numerics;

namespace CollatzConjecture
{
    internal class Program
    {
        static void Main(string[] args)
        {
            BigInteger maximum = BigInteger.Zero;
            GetNumber(out BigInteger number);

            UInt32 i = 0u;
            while (number != 1) {
                i++;
                Console.WriteLine($"{i}:\t{number}");
                number = CalcNumber(number);
                maximum = Max(number, maximum);
            }

            Console.WriteLine($"\n{i}:\t{number} | {maximum}");
        }

        static void GetNumber(out BigInteger number)
        {
            Console.Write("Введите число n: ");
            string input = Console.ReadLine() ?? "0";

            if (!BigInteger.TryParse(input, out number)) {
                Console.Error.WriteLine("Не корректный тип! Допустимый тип ввода для числа - целочисленный.");
                Environment.Exit(1);
            }

            if (number < BigInteger.Zero) {
                Console.Error.WriteLine("Не корректное значение! Допустимы толко натуральные числа.");
                Environment.Exit(1);
            }
        }

        static BigInteger Max(BigInteger a, BigInteger b)
        {
            return (a > b) ? a : b;
        }

        static BigInteger CalcNumber(BigInteger num)
        {
            if (num % 2 == 0) {
                return num / 2;
            }
            else {
                return 3 * num + 1;
            }

        }
    }
}