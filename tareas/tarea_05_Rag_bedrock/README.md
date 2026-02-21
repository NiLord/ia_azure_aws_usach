# Proyecto: Arquitectura RAG End-to-End en AWS

Este proyecto contiene la plantilla de CloudFormation para desplegar automáticamente la infraestructura necesaria para una aplicación Retrieval-Augmented Generation (RAG) en Amazon Web Services, utilizando Amazon Bedrock, S3 y una interfaz en Streamlit sobre EC2.

## Estructura del Proyecto

- `rag_infrastructure.yaml`: Plantilla de CloudFormation que provisiona:
  - Bucket S3 para almacenar los documentos.
  - Rol y Políticas de IAM (`PermisosLaboratorioBedrock`) para permitir a la EC2 invocar modelos en Bedrock y acceder a S3.
  - Security Group (`SG-Laboratorio-IA`) para permitir acceso SSH (puerto 22) y a Streamlit (puerto 8501).
  - Instancia EC2 (`t4g.micro` - ARM) configurada mediante `UserData` para descargar automáticamente un PDF desde GitHub, subirlo al bucket S3, instalar dependencias y lanzar la aplicación Streamlit en segundo plano.

## 1. Despliegue de la Infraestructura con CloudFormation

1. Inicia sesión en la consola de AWS y ve al servicio **CloudFormation**.
2. Haz clic en **Create stack** > **With new resources (standard)**.
3. En la sección "Prerequisite - Prepare template", selecciona **Template is ready**.
4. En "Specify template", selecciona **Upload a template file**, sube el archivo `rag_infrastructure.yaml` y pulsa **Next**.
5. Completa los detalles del stack:
   - **Stack name**: Ej. `LaboratorioRAG`
   - **AllowedIP**: Tu dirección IP en formato CIDR (ej. `190.32.4.96/32`) o `0.0.0.0/0` para acceso público. (puedes buscarla en https://www.cual-es-mi-ip.net/)
   - **GithubPdfUrl**: URL directa (raw) del archivo PDF que quieres cargar como conocimiento (ej. `https://raw.githubusercontent.com/NiLord/ia_azure_aws_usach/tarea_05/tareas/tarea_05_Rag_bedrock/data/documento.pdf`).
   - **InstanceType**: `t4g.micro` (por defecto, arquitectura ARM).
   - **KeyName**: Selecciona un KeyPair existente si deseas conectarte por SSH a la EC2.
   - **VpcId**: Selecciona la VPC donde quieres crear los recursos (generalmente tu VPC por defecto).
   - **SubnetId**: Selecciona una subred pública que pertenezca a la VPC que seleccionaste en el paso anterior.
6. Pulsa **Next** en las siguientes pantallas.
7. En la pantalla final, marca la casilla **I acknowledge that AWS CloudFormation might create IAM resources with custom names** y haz clic en **Submit**.
8. Espera a que el stack alcance el estado `CREATE_COMPLETE`. Ve a la pestaña **Outputs** para ver:
   - `S3BucketName`: El nombre del bucket creado.
   - `S3BucketUri`: La URI del bucket S3.
   - `StreamlitUrl`: La URL pública para acceder a tu aplicación Streamlit.

## 2. Creación del Knowledge Base en Amazon Bedrock (Paso Manual)

Una vez que CloudFormation termine, el bucket S3 ya tendrá tu documento PDF cargado. El siguiente paso es configurar el motor de conocimiento en Bedrock.

1. Ve a la consola de **Amazon Bedrock**.
2. Asegúrate de estar en la región correcta (ej. `us-east-1`).
3. En el menú lateral izquierdo, ve a **Builder tools > Knowledge bases** y haz clic en **Create knowledge base**.
4. **Paso 1 (Detalles):**
   - **Name**: `kb-laboratorio-ia`
   - **IAM Permissions**: Deja seleccionado `Create and use a new service role`.
5. **Paso 2 (Configurar Origen de Datos):**
   - **Data Source**: Selecciona `Amazon S3`.
   - **S3 URI**: Haz clic en `Browse S3` y selecciona el bucket creado por CloudFormation (puedes ver el nombre en los Outputs de CloudFormation).
   - **Parsing Strategy**: Mantén `Default parser`.
   - **Chunking Strategy**: Mantén `Default chunking`.
6. **Paso 3 (Vector Store):**
   - **Embedding Model**: Elige `Titan Text Embeddings v2`.
   - **Vector Store**: Elige `Quick create a new vector store`.
   - **Vector store type**: Elige `OpenSearch Serverless`.
7. Finaliza la creación de la Knowledge Base.
8. **Muy Importante**: Una vez creada, ve a la sección Data source y pulsa el botón **Sync** para que Bedrock procese el PDF de tu bucket S3.
9. **Anota el Knowledge Base ID** (un código alfanumérico como `US6LSEJEGC`).

## 3. Uso de la Aplicación Web

1. Abre la URL de Streamlit obtenida en los **Outputs** de CloudFormation (`http://<IpPublicaEC2>:8501`).
2. Ingresa el **Knowledge Base ID** que anotaste en el paso anterior.
3. Realiza preguntas sobre el documento que se subió al Knowledge Base en el chat. La IA te responderá utilizando la información del PDF mediante RAG y el modelo Nova Lite.

## 4. Limpieza de Recursos (Clean Up)

Para evitar cargos innecesarios en AWS:
1. Elimina la **Knowledge Base** en Amazon Bedrock (asegúrate de eliminar también el Vector Store de OpenSearch Serverless creado automáticamente).
2. Ve al bucket S3 creado y **vacía su contenido** (elimina el archivo `documento.pdf`).
3. Ve a **CloudFormation**, selecciona tu stack (`LaboratorioRAG`) y pulsa **Delete**. Esto eliminará automáticamente la instancia EC2, el Security Group, el Rol de IAM y el bucket S3 (si está vacío).

## 5. Conclusiones

Este proyecto permitió implementar de forma práctica una arquitectura de **Retrieval-Augmented Generation (RAG)** completa en AWS, integrando múltiples servicios en una solución cohesiva para la consulta inteligente de documentos privados.

### Aprendizajes Técnicos

- **Infraestructura como Código (IaC):** El uso de AWS CloudFormation demostró ser fundamental para garantizar despliegues reproducibles y limpios. Parametrizar la plantilla (VPC, Subnet, URL del PDF, tipo de instancia) permite reutilizarla en distintos entornos sin modificar el código base.

- **Arquitectura RAG:** Se comprendió el flujo completo del patrón RAG: los documentos se vectorizan mediante un modelo de embeddings (`Titan Text Embeddings V2`), se almacenan en una base de datos vectorial (`OpenSearch Serverless`) y, ante una consulta del usuario, el sistema recupera los fragmentos más relevantes para enriquecer el contexto del modelo generativo (`Amazon Nova Lite`), produciendo respuestas fundamentadas en la información privada.

- **Seguridad en AWS:** La correcta configuración de roles IAM con el principio de mínimo privilegio es esencial. El rol de la EC2 solo tiene permisos sobre su propio bucket S3 y las acciones de Bedrock estrictamente necesarias, evitando exposición innecesaria.

- **Arquitectura ARM en EC2:** El uso de instancias `t4g.micro` (arquitectura ARM Graviton) ofrece hasta un 40% mejor relación precio-rendimiento respecto a instancias x86 equivalentes, siendo una opción eficiente para cargas de trabajo de aplicaciones web ligeras como Streamlit.

### Desafíos Encontrados

- **Cuotas de servicio en AWS Bedrock:** Se identificó que las cuentas nuevas o con configuraciones atípicas pueden tener la cuota de inferencia On-demand de los modelos Titan Embeddings establecida en `0` (en lugar del valor por defecto de `6.000 RPM`), causando errores `429 Too Many Requests` durante la sincronización del Knowledge Base. La solución requiere abrir un caso de soporte con AWS para restablecer la cuota al valor predeterminado.

- **Gestión de subredes en VPC:** La ausencia de subredes por defecto en la VPC predeterminada requirió parametrizar explícitamente el `VpcId` y `SubnetId` en la plantilla CloudFormation, evidenciando la importancia de no asumir configuraciones de red predeterminadas en entornos de producción.

### Valor de la Solución

La arquitectura implementada resuelve un problema real y frecuente en organizaciones: **consultar información privada y sensible sin exponerla a modelos de IA externos**. Al mantener los documentos en S3 dentro de la propia cuenta de AWS y procesar las consultas íntegramente en Bedrock, se garantiza la privacidad y el control total sobre los datos, cumpliendo con requisitos de seguridad y cumplimiento normativo que modelos públicos no pueden satisfacer.
