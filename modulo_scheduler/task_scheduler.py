"""
Módulo Scheduler - Agendamento de Tarefas
"""

import logging
import time
from datetime import datetime
from typing import Callable, Optional
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import sys
import os

# Adiciona o diretório raiz ao path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from config.config import Config
except ImportError:
    # Fallback para configuração básica
    class Config:
        FUSO_HORARIO = "America/Sao_Paulo"
        HORA_EXECUCAO = "07:00"


class TaskScheduler:
    """Agendador de tarefas usando APScheduler"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Inicializa o agendador
        
        Args:
            config: Objeto de configuração
        """
        self.config = config or Config()
        self.scheduler = BlockingScheduler(timezone=pytz.timezone(self.config.FUSO_HORARIO))
        self.setup_logging()
    
    def setup_logging(self):
        """Configura logging"""
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, 'scheduler.log')),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def agendar_tarefa_diaria(
        self,
        funcao: Callable,
        hora: str = "07:00",
        minuto: str = "00"
    ):
        """
        Agenda uma tarefa para execução diária
        
        Args:
            funcao: Função a ser executada
            hora: Hora da execução (formato HH)
            minuto: Minuto da execução (formato MM)
        """
        try:
            hora_int = int(hora.split(':')[0]) if ':' in hora else int(hora)
            minuto_int = int(minuto) if minuto else 0
            
            if ':' in hora:
                hora_int, minuto_int = map(int, hora.split(':'))
            
            self.scheduler.add_job(
                funcao,
                trigger=CronTrigger(hour=hora_int, minute=minuto_int),
                id='tarefa_diaria_bacen',
                name='Monitoramento Diário BACEN',
                replace_existing=True
            )
            
            self.logger.info(f"Tarefa agendada para execução diária às {hora_int:02d}:{minuto_int:02d}")
            
        except Exception as e:
            self.logger.error(f"Erro ao agendar tarefa: {str(e)}")
            raise
    
    def executar(self):
        """Inicia o agendador em modo bloqueante"""
        try:
            self.logger.info("Iniciando agendador de tarefas...")
            self.logger.info(f"Fuso horário: {self.config.FUSO_HORARIO}")
            self.logger.info(f"Horário de execução: {self.config.HORA_EXECUCAO}")
            
            self.scheduler.start()
            
        except KeyboardInterrupt:
            self.logger.info("Agendador interrompido pelo usuário")
            self.scheduler.shutdown()
        except Exception as e:
            self.logger.error(f"Erro no agendador: {str(e)}")
            self.scheduler.shutdown()
            raise
    
    def adicionar_tarefa_manual(self, funcao: Callable, **trigger_args):
        """
        Adiciona uma tarefa com trigger customizado
        
        Args:
            funcao: Função a ser executada
            **trigger_args: Argumentos para o trigger
        """
        self.scheduler.add_job(funcao, **trigger_args)
    
    def listar_tarefas(self):
        """Lista todas as tarefas agendadas"""
        jobs = self.scheduler.get_jobs()
        self.logger.info(f"Tarefas agendadas: {len(jobs)}")
        for job in jobs:
            self.logger.info(f"  - {job.id}: {job.name} - Próxima execução: {job.next_run_time}")
        return jobs
    
    def remover_tarefa(self, job_id: str):
        """
        Remove uma tarefa agendada
        
        Args:
            job_id: ID da tarefa
        """
        try:
            self.scheduler.remove_job(job_id)
            self.logger.info(f"Tarefa {job_id} removida")
        except Exception as e:
            self.logger.error(f"Erro ao remover tarefa {job_id}: {str(e)}")

