#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse

def createParser():
    parser = argparse.ArgumentParser(
            prog = 'ArSi Analayzer',
            description = u'''Программа для анализа статистики собранной в процессе сетевого сканирования.''',
            epilog = u'''(c) Vinigrator 2016. Автор программы, как всегда, не несет никакой ответственности ни за что...'''
            )

    parser.add_argument('name', nargs='?',
                        help = u'''Название общей части файлов статистики.
                               Формат записи: имя_файлов_N''')

    parser.add_argument('-n','--num', default='1',
                        help=u'''Количество анализируемых файлов.''')

    parser.add_argument('-an', '--analysis-file-name', default='analysis.txt',
                        help=u'''Имя файла с инфой анализа.''')

    parser.add_argument('-oat', '--only-anomal-text', action='store_const', const=True, default=False,
                        help=u'''Вывести только файл аномальной статистики.''')

    parser.add_argument('-pll', '--print-length-list', action='store_const', const=True, default=False,
                        help=u'''Вывести длину списков.''')

    parser.add_argument('-adp', '--agreagate-data-picture', dest='adp', action='store_const', const=True, default=False,
                        help=u'''Создать файл с агрегацией данных.''')
    #                    help=u'''ICMP сканирование''')
    #parser.add_argument('-p','--ports', default='-65535',
    #                    help = u'''Список сканируемых портов. Порты разделяются символом ','.
    #                           Диапозон портов задаётся посредством символа '-'.
    #                           Пример: 21-23,80,8080.
    #                           Будут просканированы порты 21,22,23,80,8080.
    #                           По умолчанию: все порты''',
    #                    metavar = u'ПОРТЫ')

    #parser.add_argument('-hp','--handler_ports', default='',
    #                    help = u'''Список портов, для которых необходим дополнительный обработчик. Порты разделяются символом ','.
    #                           Диапозон портов задаётся посредством символа '-'.
    #                           Пример: 21-23,80,8080.
    #                           Будут просканированы порты 21,22,23,80,8080.
    #                           ''',
    #                    metavar = u'ПОРТЫ')

    #parser.add_argument('-ahp', '--all_hendler_ports', action='store_const', const=True, default=False,
    #                    help = u'''Обработчики необходимы для всех портов, для которых идёт сканирование.''')

    #parser.add_argument('-icmp', '--ICMP', action='store_const', const=True, default=False,
    #                    help=u'''ICMP сканирование''')

    #parser.add_argument('-g', '--goodbye', action='store_const', const=True, default=False)
    #parser.add_argument('-udp', action='store_true', default=False,
    #                    help = u'''Сканирование UDP-портов.''')

    #parser.add_argument('-l', '--log', '--logFile', type=argparse.FileType('a'),
    #                   help = u'''Путь до файла, куда будут внесены данные лога.''',
    #                   metavar=u'Путь_до_файла')

    #parser.add_argument('-l', '--log', '--logFile', default="arsi_log.txt",
    #                   help = u'''Путь до файла, куда будут внесены данные лога.''',
    #                   metavar=u'Путь_до_файла')

    return parser