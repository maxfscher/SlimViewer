from datetime import timedelta
from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_project


class LocalWSI2DCMOperator(KaapanaBaseOperator):

    def __init__(self,
                 dag,
                 execution_timeout=timedelta(seconds=6000),
                 *args, **kwargs
                 ):

        super().__init__(
            dag=dag,
            name='wsi2dcm',
            image=f"{default_registry}/pixelmedimage:0.1.0",# running version tag:5.0, stable previous version/wsi2dcm:6.0
            image_pull_secrets=["registry-secret"],
            execution_timeout=execution_timeout,
            #cmds=['tail'],
            #arguments=['-f', '/dev/null'],
            ram_mem_mb=12000,
            ram_mem_mb_lmt=12000,
            *args,
            **kwargs
        )
