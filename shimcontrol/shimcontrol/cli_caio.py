import argparse
import sys

from tabulate import tabulate

from shimcontrol.lib import ADCCommandSet, DACCommandSet, dac_code_to_voltage

def subcommand(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)

            return False

        return True

    return func


@subcommand
def get_action(args):
    adc = ADCCommandSet(5) #construtor do Set de comandos do ADC, inicializa com 5 modulos AD.
    adc.from_read(args.channelsa) #coloca no campo comandos do objeto adc a sequencia ordenada dos canais a serem lidos.  

    results = adc.execute() 

    print(tabulate(
        [(ch, '{:1.3f}'.format(r)) for ch, r in results],
        headers=['Channel', 'Voltage'],
    ))

@subcommand
def set_action(args):

    dac = DACCommandSet(5) #Cria Objeto que especifica 5 DACs plugados(Comandos e Grupos não inicializados).
    dac.from_write(args.channels) #Prepara dados para a interface Serial SPI
    dac.execute()

    outputs = [
        (channel, code, dac_code_to_voltage(code))
        for channel, code in args.channels
    ]

    print(tabulate(
     
   outputs,
        headers=['Channel', 'Value', 'Voltage'],
    ))

@subcommand
def list_action(args):
    print(args)


class ChannelValuesAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        channels = []
        for pair in values:
            channel, value = pair.split('=')
            channels.append((
                int(channel), int(value, 0)
            ))

        setattr(namespace, self.dest, channels)

def build_parser():
    parser = argparse.ArgumentParser() #cria objeto parser 

    subparsers = parser.add_subparsers() #cria objeto subparser herdado de parser

    list_parser = subparsers.add_parser('list', help='List channels') #cria objeto parser com nome list_parser advindo da classe subparser (parser para o comando 'list')
    list_parser.set_defaults(func=list_action) #Associa função 'list_action' como default para o comando list

    get_parser = subparsers.add_parser('get', help='Get channel data') #cria parser para o comando 'get'
    get_parser.set_defaults(func=get_action) #Associa função 'get_action' como default para o comando get
    get_parser.add_argument('channels', nargs='+', type=int) #Adiciona argumento channels para o comando get, numero de argumentos deve ser maior que um, e convertidos em inteiros.

    set_parser = subparsers.add_parser('set', help='Set channel data') 
    set_parser.set_defaults(func=set_action)
    set_parser.add_argument('channels', nargs='+', action=ChannelValuesAction)

    return parser

def main():
    parser = build_parser() #cria objeto parser

    args = parser.parse_args() #Passa os argumentos a serem recebidos na linha de comando, assim como os argumentos dos argumentos. (Desconheço o mecanismo que o objeto parser possui para registrar tais informações) 

    if hasattr(args, 'func'): #(Caso dentro dos argumentos haja funções registradas)
        if args.func(args):
            sys.exit(0) #Se a função executada executar com sucesso sai sem registrar erro.
        else:
            sys.exit(1) #Caso contrario ocorre um erro.
    else:
        parser.print_help() #Caso contrario o usuario nao entrou com os argumentos corretos, printar help do parser.

if __name__ == '__main__':
    main()
