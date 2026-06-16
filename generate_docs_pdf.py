import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):
        # Capa (Página 1) - Desenho completo no Canvas
        if self._pageNumber == 1:
            self.saveState()
            # Fundo Azul Escuro no topo (Banner principal)
            self.setFillColor(colors.HexColor("#1A365D"))
            self.rect(0, 460, 595.27, 382, fill=1, stroke=0)
            
            # Linha de Destaque Teal/Verde água
            self.setFillColor(colors.HexColor("#319795"))
            self.rect(0, 440, 595.27, 20, fill=1, stroke=0)
            
            # Textos do Topo (Brancos)
            self.setFillColor(colors.white)
            self.setFont("Helvetica-Bold", 38)
            self.drawString(54, 680, "PEOPLEFLOW")
            
            self.setFont("Helvetica-Bold", 14)
            self.setFillColor(colors.HexColor("#E2E8F0"))
            self.drawString(54, 640, "SISTEMA DE GESTÃO DE COLABORADORES E AUDITORIA")
            
            self.setFont("Helvetica-Bold", 11)
            self.setFillColor(colors.HexColor("#81E6D9"))
            self.drawString(54, 600, "DOCUMENTAÇÃO TÉCNICA OFICIAL DO SISTEMA")
            
            self.setFont("Helvetica-Oblique", 11)
            self.setFillColor(colors.HexColor("#CBD5E0"))
            self.drawString(54, 550, "Arquitetura MVC com Camada de Serviços, MySQL, MongoDB e Geração de XML/PDF")
            
            # Textos do Corpo da Capa (Preto/Cinza)
            self.setFillColor(colors.HexColor("#2D3748"))
            self.setFont("Helvetica-Bold", 13)
            self.drawString(54, 380, "Sumário do Conteúdo Documentado:")
            
            self.setFont("Helvetica", 10.5)
            self.setFillColor(colors.HexColor("#4A5568"))
            topics = [
                "1. Tema e Objetivo Geral do Sistema",
                "2. Regras de Negócio e Validações de Dados",
                "3. Arquitetura do Sistema e Estrutura MVC",
                "4. Explicação de Interfaces (IDAO, IService, IController) e Classes",
                "5. Camada de Serviços e Centralização de Regras de Negócio",
                "6. Mapeamento do Banco de Dados Relacional MySQL",
                "7. Estrutura e Auditoria NoSQL MongoDB (Acessos, CRUD e Erros)",
                "8. Geração e Exportação de Logs no Formato XML",
                "9. Relatórios de Colaboradores Gerados Dinamicamente em PDF",
                "10. Gráficos de Indicadores e Painel de Monitoramento (Chart.js)",
                "11. Manual Passo a Passo para Execução da Aplicação (Docker)",
                "12. Dicionário Completo de Rotas e Endpoints da API"
            ]
            y = 350
            for topic in topics:
                self.drawString(70, y, topic)
                y -= 20
                
            # Detalhes de Rodapé da Capa
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.7)
            self.line(54, 100, 541, 100)
            
            self.setFillColor(colors.HexColor("#718096"))
            self.setFont("Helvetica-Bold", 9)
            self.drawString(54, 80, "DESENVOLVIMENTO DE SOFTWARE ACADÊMICO")
            self.drawString(54, 65, "AMBIENTE: Python 3.12 | Flask | MySQL | MongoDB | Docker")
            
            self.drawRightString(541, 80, "MÉTRICAS E PADRÕES")
            self.drawRightString(541, 65, "Maio de 2026")
            
            self.restoreState()
            return
            
        # Páginas Seguintes (Cabeçalho e Rodapé)
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Cabeçalho
        self.drawString(54, 785, "PeopleFlow — Manual de Documentação Técnica")
        self.drawRightString(541, 785, "Arquitetura MVC & Multi-banco de Dados")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 777, 541, 777)
        
        # Rodapé
        self.line(54, 45, 541, 45)
        self.drawString(54, 30, "Documentação oficial elaborada em conformidade com os requisitos de sistema.")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(541, 30, page_text)
        
        self.restoreState()

def build_pdf():
    pdf_filename = "documentacao.pdf"
    
    # Criando o documento A4 Retrato
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=80,
        bottomMargin=65
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=15,
        keepWithNext=True
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#2D3748"),
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )
    
    list_style = ParagraphStyle(
        'CustomList',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#2D3748"),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1A202C"),
        backColor=colors.HexColor("#EDF2F7"),
        borderColor=colors.HexColor("#E2E8F0"),
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=10
    )
    
    table_text = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#2D3748")
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.white
    )
    
    story = []
    
    # --- PÁGINA 1: CAPA ---
    # Como a capa é gerada inteiramente no NumberedCanvas, colocamos apenas um PageBreak para o story começar na Página 2
    story.append(PageBreak())
    
    # --- PÁGINA 2: TEMA, OBJETIVO E REGRAS DE NEGÓCIO ---
    story.append(Paragraph("DOCUMENTAÇÃO TÉCNICA DO PEOPLEFLOW", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1A365D"), spaceAfter=15))
    
    story.append(Paragraph("1. Tema Escolhido e Objetivo Geral do Sistema", h1_style))
    story.append(Paragraph(
        "O <b>PeopleFlow</b> é um sistema de Gestão de Recursos Humanos e Auditoria de Ações Administrativas. "
        "Seu principal objetivo é fornecer uma solução integrada, estável, escalável e segura para gerenciar os colaboradores de "
        "uma organização, categorizando-os por departamentos, cargos e competências (habilidades). O sistema resolve a necessidade "
        "clássica de consolidação de informações funcionais em uma empresa, automatizando rotinas cadastrais ao mesmo tempo em "
        "que atende a requisitos avançados de banco de dados híbrido (com MySQL para dados transacionais consistentes e "
        "MongoDB para registros dinâmicos e flexíveis de auditoria permanente).",
        body_style
    ))
    
    story.append(Paragraph("2. Regras de Negócio Principais", h1_style))
    story.append(Paragraph(
        "Para manter a consistência operacional, integridade dos dados e conformidade do sistema, foram estabelecidas as seguintes "
        "regras de negócio fundamentais:",
        body_style
    ))
    story.append(Paragraph("• <b>Controle de Acesso Centralizado (Autenticação):</b> Apenas usuários administrativos cadastrados "
                           "podem interagir com o sistema. Toda rota privada é protegida por um middleware de autenticação baseado em sessão. "
                           "As senhas de acesso administrativo são criptografadas em hash criptográfico seguro (SHA256 via "
                           "Werkzeug <i>generate_password_hash</i>) no banco de dados e verificadas por verificação matemática na tentativa de login.", list_style))
    story.append(Paragraph("• <b>Unicidade do Colaborador:</b> Cada colaborador cadastrado é indexado de forma exclusiva. O sistema "
                           "impede a inserção de colaboradores com o mesmo Documento (CPF/Registro) ou com o mesmo endereço de e-mail.", list_style))
    story.append(Paragraph("• <b>Relacionamento Hierárquico Obrigatório:</b> Um colaborador deve obrigatoriamente possuir um cargo válido. "
                           "Da mesma forma, um cargo deve pertencer de forma indissociável a um departamento ativo no organograma da empresa. "
                           "Não é possível cadastrar colaboradores órfãos de cargo.", list_style))
    story.append(Paragraph("• <b>Validação Rigorosa de Imagens (Uploads):</b> O colaborador pode opcionalmente ter uma foto de perfil. "
                           "A foto passa por um validador de extensão (apenas webp, png, jpg, jpeg são aceitos). O arquivo físico é renomeado no "
                           "servidor para um hash único (UUIDv4) para prevenir a execução de scripts maliciosos ou sobrescrita acidental de fotos.", list_style))
    story.append(Paragraph("• <b>Auditoria In violável (Logs):</b> Toda operação de escrita em qualquer entidade crítica do sistema "
                           "(Colaboradores, Departamentos, Cargos, Habilidades) gera uma entrada de auditoria em tempo real no MongoDB "
                           "com o e-mail do usuário logado, timestamp UTC, ação, tabela afetada, id e o payload do objeto modificado.", list_style))
    
    story.append(PageBreak())
    
    # --- PÁGINA 3: ARQUITETURA MVC IMPLEMENTADA ---
    story.append(Paragraph("3. Estrutura MVC Implementada no Sistema", h1_style))
    story.append(Paragraph(
        "Diferente de frameworks altamente estruturados como o Laravel, o Flask é um microframework que não impõe "
        "um padrão organizacional rígido. Por este motivo, o PeopleFlow foi planejado seguindo uma <b>arquitetura MVC com Service Layer "
        "e Repository/DAO</b> altamente modular, permitindo a separação explícita de responsabilidades em camadas:",
        body_style
    ))
    
    # Lista de pastas e papéis
    story.append(Paragraph("• <b>Models (app/models/):</b> Define a estrutura de dados relacional. Cada model representa uma tabela do MySQL "
                           "mapeada por objetos Python utilizando SQLAlchemy. Define as regras de relacionamentos e restrições de chaves estrangeiras.", list_style))
    story.append(Paragraph("• <b>Views (app/templates/ & app/static/):</b> Camada de interface de usuário. Utiliza templates HTML compilados no "
                           "servidor via Jinja2, folhas de estilo CSS puro estruturadas em tokens e arquivos JavaScript puros para controle "
                           "dinâmico e rendering do gráfico interativo com Chart.js.", list_style))
    story.append(Paragraph("• <b>Controllers (app/controllers/):</b> Responsável por tratar a requisição HTTP. O controlador lê parâmetros, "
                           "aciona a camada de serviços (Service Layer) apropriada para processamento de negócios e decide qual View (HTML) "
                           "renderizar ou qual resposta JSON retornar.", list_style))
    story.append(Paragraph("• <b>Services (app/services/):</b> Centraliza toda a inteligência e lógica de negócio. Realiza validações "
                           "de dados que excedem escopo de banco, gerencia uploads de fotos, gerencia conexões e gravações de logs no MongoDB, "
                           "serializa logs em XML, gera PDFs dinamizados com a biblioteca ReportLab e trata importações/exportações de dados em JSON.", list_style))
    story.append(Paragraph("• <b>DAOs (app/daos/):</b> Camada de persistência relacional. Isola as queries e manipulações de banco de dados MySQL "
                           "via ORM, evitando que a lógica de negócios ou controladores lidem diretamente com sessões ou entidades SQLAlchemy.", list_style))
    story.append(Paragraph("• <b>Routers (app/routers/):</b> Define as rotas HTTP e endpoints da aplicação organizados por blueprints temáticos. "
                           "Mapeia as URLs da aplicação diretamente para as funções correspondentes nos controladores.", list_style))
    story.append(Paragraph("• <b>Middlewares (app/middlewares/):</b> Interceptadores de requisição HTTP que gerenciam a autenticação de rotas privadas, "
                           "realizam validações genéricas de formulários corporativos, registram logs de requisições e tratam exceções não capturadas.", list_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Fluxo de Controle de Requisições:", h2_style))
    story.append(Paragraph(
        "A requisição HTTP atinge o servidor Flask -> Passa pelos Middlewares (Autenticação/Validação) -> Mapeada pelo Blueprint (Router) "
        "-> Executa a ação do Controller -> O Controller invoca o Service correspondente -> O Service processa a regra de negócios e chama o DAO "
        "-> O DAO interage com o Model do SQLAlchemy persistindo no MySQL -> O Service registra a ação disparando um log para o MongoDB "
        "-> O Controller recebe o retorno da operação e repassa a View compilada em HTML via Jinja2 ou serializada em JSON para o cliente.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # --- PÁGINA 4: EXPLICAÇÃO DAS INTERFACES E CLASSES ---
    story.append(Paragraph("4. Explicação das Interfaces e Classes Implementadoras", h1_style))
    story.append(Paragraph(
        "Para garantir o baixo acoplamento e o princípio de inversão de dependência, o sistema implementa explicitamente contratos de código "
        "utilizando a biblioteca <i>abc.ABC</i> (Abstract Base Classes) do Python. Estes contratos definem a estrutura que as classes "
        "concretas devem seguir de forma obrigatória.",
        body_style
    ))
    
    story.append(Paragraph("A Interface de Persistência: IDAO (dao_interface.py)", h2_style))
    story.append(Paragraph(
        "Define os métodos padrão que qualquer objeto de acesso a dados (DAO) do sistema precisa implementar para persistir entidades no MySQL:",
        body_style
    ))
    story.append(Paragraph(
        "class IDAO(ABC):\n"
        "    @abstractmethod\n"
        "    def find_all(self): pass\n"
        "    @abstractmethod\n"
        "    def find_by_id(self, id): pass\n"
        "    @abstractmethod\n"
        "    def create(self, data): pass\n"
        "    @abstractmethod\n"
        "    def update(self, id, data): pass\n"
        "    @abstractmethod\n"
        "    def delete(self, id): pass",
        code_style
    ))
    story.append(Paragraph(
        "<b>Classes que a implementam:</b> Implementada pela classe genérica <b>BaseDAO</b> (base_dao.py), que fornece "
        "toda a implementação padrão utilizando o Flask-SQLAlchemy global (db.session). As classes especializadas "
        "<b>EmployeeDAO</b>, <b>DepartmentDAO</b>, <b>PositionDAO</b>, <b>SkillDAO</b> e <b>UserDAO</b> estendem "
        "BaseDAO para herdar os métodos comuns e implementar métodos especializados (como consultas complexas e buscas parametrizadas).",
        body_style
    ))
    
    story.append(Paragraph("A Interface de Negócios: IService (service_interface.py)", h2_style))
    story.append(Paragraph(
        "Define as assinaturas fundamentais que as classes de serviço administrativas devem prover para o ecossistema:",
        body_style
    ))
    story.append(Paragraph(
        "class IService(ABC):\n"
        "    @abstractmethod\n"
        "    def list(self): pass\n"
        "    @abstractmethod\n"
        "    def get(self, id): pass\n"
        "    @abstractmethod\n"
        "    def store(self, data): pass\n"
        "    @abstractmethod\n"
        "    def update(self, id, data): pass\n"
        "    @abstractmethod\n"
        "    def delete(self, id): pass",
        code_style
    ))
    story.append(Paragraph(
        "<b>Classes que a implementam:</b> Implementada formalmente pela classe <b>EmployeeService</b> (employee_service.py). "
        "Ela realiza a validação de regras de negócios complexas do colaborador, processa uploads de imagens, converte strings para datas "
        "e consome o EmployeeDAO, encapsulando opcionalmente chamadas de log em tempo real.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # --- PÁGINA 5: INTERFACE ICONTROLLER E CAMADA DE SERVIÇOS ---
    story.append(Paragraph("A Interface de Controle: IController (controller_interface.py)", h2_style))
    story.append(Paragraph(
        "Define o esqueleto obrigatório de métodos que os controladores CRUD do sistema devem possuir para responder à requisições web:",
        body_style
    ))
    story.append(Paragraph(
        "class IController(ABC):\n"
        "    @abstractmethod\n"
        "    def index(self): pass\n"
        "    @abstractmethod\n"
        "    def show(self, id): pass\n"
        "    @abstractmethod\n"
        "    def create(self): pass\n"
        "    @abstractmethod\n"
        "    def store(self): pass\n"
        "    @abstractmethod\n"
        "    def edit(self, id): pass\n"
        "    @abstractmethod\n"
        "    def update(self, id): pass\n"
        "    @abstractmethod\n"
        "    def destroy(self, id): pass",
        code_style
    ))
    story.append(Paragraph(
        "<b>Classes que a implementam:</b> Implementada pelos controladores <b>EmployeeController</b>, <b>DepartmentController</b>, "
        "<b>PositionController</b> e <b>SkillController</b>. Esses controladores realizam a interface entre o HTTP e os serviços correspondentes, "
        "usando flash messages para interagir com o cliente do Flask e decidindo sobre o redirecionamento ou o render do template HTML.",
        body_style
    ))
    
    story.append(Paragraph("5. Explicação dos Services (Regras de Negócio Separadas)", h1_style))
    story.append(Paragraph(
        "A arquitetura isola completamente a inteligência de negócios na Service Layer. Isso impede que controladores possuam lógica "
        "complexa de validação ou fiquem acoplados a conexões de bancos de dados. Principais lógicas distribuídas por serviços:",
        body_style
    ))
    story.append(Paragraph("• <b>EmployeeService:</b> Trata a inserção, edição e exclusão de colaboradores. Formata nomes, limpa e padroniza e-mails "
                           "para caixa baixa (lowercase), padroniza números telefônicos e documentos. Efetua a verificação e armazenamento de arquivos de fotos "
                           "utilizando a biblioteca <i>secure_filename</i>, gerando um identificador hexadecimal único com <i>uuid.uuid4</i>. "
                           "Sincroniza dinamicamente as competências (Skills) associadas via tabela intermediária relacional e invoca o <i>LogService</i> "
                           "para gravar os metadados da modificação no banco de auditoria MongoDB.", list_style))
    story.append(Paragraph("• <b>AuthService:</b> Gerencia o fluxo de controle de login e registro administrativo. Recebe dados planos de credenciais, "
                           "pesquisa o usuário cadastrado no MySQL via UserRepository, gera o hash criptográfico seguro irreversível de senha no cadastro e "
                           "valida a assinatura da senha plana no login. Registra o e-mail ativo do usuário na sessão global do Flask (`session`).", list_style))
    story.append(Paragraph("• <b>LogService:</b> Abstração de log do MongoDB. Define os schemas dos documentos JSON de logs, salvando registros corporativos "
                           "como tipo de evento, timestamp, usuário que executou a ação, tabela do banco relacional associada, ID do registro, "
                           "detalhes adicionais (como dados modificados), endereço IP remoto e User-Agent do navegador.", list_style))
    story.append(Paragraph("• <b>JsonService:</b> Realiza importações e exportações estruturadas de tabelas em arquivos `.json`. Executa validações de dados "
                           "recebidos de arquivos JSON externos (garantindo que campos obrigatórios existam e chaves estrangeiras de cargos ou "
                           "departamentos correspondam a IDs existentes) antes de autorizar a inserção de registros no MySQL.", list_style))
    story.append(Paragraph("• <b>XmlService & PdfService:</b> Serviços especializados em exportação e apresentação física de relatórios estruturados, "
                           "isolando a complexidade de escrita em tags XML e as tabelas com coordenadas de pontos da biblioteca ReportLab.", list_style))
    
    story.append(PageBreak())
    
    # --- PÁGINA 6: ESTRUTURA DO BANCO DE DADOS MYSQL ---
    story.append(Paragraph("6. Estrutura do Banco de Dados MySQL (Tabelas e Relacionamentos)", h1_style))
    story.append(Paragraph(
        "A persistência dos dados transacionais do sistema é mantida em um banco de dados relacional MySQL 8. "
        "A estrutura lógica foi modelada para garantir normalização, indexação eficiente de e-mails/documentos e integridade "
        "referencial rigorosa utilizando restrições de chaves estrangeiras (FOREIGN KEY).",
        body_style
    ))
    
    # Tabela com as informações das tabelas e colunas
    mysql_data = [
        [Paragraph("<b>Tabela</b>", table_header), Paragraph("<b>Coluna / Tipo</b>", table_header), Paragraph("<b>Nulo</b>", table_header), Paragraph("<b>Índice / Restrição</b>", table_header), Paragraph("<b>Descrição / Chave Estrangeira</b>", table_header)],
        [Paragraph("users", table_text), Paragraph("id (INT)<br/>name (VARCHAR)<br/>email (VARCHAR)<br/>password (VARCHAR)", table_text), Paragraph("Não<br/>Não<br/>Não<br/>Não", table_text), Paragraph("PK<br/>-<br/>UNIQUE, INDEX<br/>-", table_text), Paragraph("Administradores do sistema. Email usado no Login. Senha salva em hash criptográfico.", table_text)],
        [Paragraph("departments", table_text), Paragraph("id (INT)<br/>name (VARCHAR)<br/>description (TEXT)", table_text), Paragraph("Não<br/>Não<br/>Sim", table_text), Paragraph("PK<br/>UNIQUE, INDEX<br/>-", table_text), Paragraph("Departamentos corporativos da empresa (ex: TI, RH, Vendas, Financeiro).", table_text)],
        [Paragraph("positions", table_text), Paragraph("id (INT)<br/>department_id (INT)<br/>name (VARCHAR)<br/>description (TEXT)", table_text), Paragraph("Não<br/>Não<br/>Não<br/>Sim", table_text), Paragraph("PK<br/>INDEX<br/>-<br/>-", table_text), Paragraph("Cargos associados. <b>FK: departments.id</b>.<br/>ondelete='RESTRICT', onupdate='CASCADE'", table_text)],
        [Paragraph("employees", table_text), Paragraph("id (INT)<br/>position_id (INT)<br/>name (VARCHAR)<br/>email (VARCHAR)<br/>phone (VARCHAR)<br/>document (VARCHAR)<br/>birth_date (DATE)<br/>admission_date (DATE)<br/>status (VARCHAR)<br/>photo_path (VARCHAR)", table_text), Paragraph("Não<br/>Não<br/>Não<br/>Não<br/>Sim<br/>Não<br/>Sim<br/>Não<br/>Não<br/>Sim", table_text), Paragraph("PK<br/>INDEX<br/>-<br/>UNIQUE, INDEX<br/>-<br/>UNIQUE, INDEX<br/>-<br/>-<br/>INDEX<br/>-", table_text), Paragraph("Colaboradores cadastrados. <b>FK: positions.id</b>.<br/>ondelete='RESTRICT', onupdate='CASCADE'.<br/>Status padrão: 'ativo'.", table_text)],
        [Paragraph("skills", table_text), Paragraph("id (INT)<br/>name (VARCHAR)", table_text), Paragraph("Não<br/>Não", table_text), Paragraph("PK<br/>UNIQUE, INDEX", table_text), Paragraph("Habilidades e competências corporativas (ex: Python, Flask, Liderança).", table_text)],
        [Paragraph("employee_skills", table_text), Paragraph("id (INT)<br/>employee_id (INT)<br/>skill_id (INT)<br/>created_at (DATETIME)", table_text), Paragraph("Não<br/>Não<br/>Não<br/>Não", table_text), Paragraph("PK<br/>INDEX<br/>INDEX<br/>-", table_text), Paragraph("Tabela intermediária N:N.<br/><b>FK: employees.id</b> (ondelete='CASCADE')<br/><b>FK: skills.id</b> (ondelete='RESTRICT')<br/>UQ: (employee_id, skill_id)", table_text)]
    ]
    
    mysql_table = Table(mysql_data, colWidths=[65, 105, 35, 95, 187])
    mysql_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    story.append(mysql_table)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Relacionamentos Lógicos:", h2_style))
    story.append(Paragraph("• <b>Departments (1) -> Positions (N):</b> Um departamento abriga múltiplos cargos. A exclusão de um departamento é impedida (RESTRICT) se houver cargos vinculados a ele.", list_style))
    story.append(Paragraph("• <b>Positions (1) -> Employees (N):</b> Um cargo é associado a múltiplos colaboradores. A exclusão do cargo é bloqueada (RESTRICT) se colaboradores estiverem alocados nele.", list_style))
    story.append(Paragraph("• <b>Employees (N) <-> Skills (N) via EmployeeSkills:</b> Um colaborador pode possuir várias habilidades, e uma habilidade pode pertencer a vários colaboradores. Se um colaborador for excluído, sua associação na tabela intermediária é removida automaticamente (CASCADE); se a habilidade for excluída, o banco barra a remoção (RESTRICT) se houver vínculo ativo.", list_style))
    
    story.append(PageBreak())
    
    # --- PÁGINA 7: MONGODB E LOGS ---
    story.append(Paragraph("7. Explicação do MongoDB e a Estrutura dos Logs", h1_style))
    story.append(Paragraph(
        "A fim de implementar um log de auditoria corporativo seguro, escalável e robusto sem onerar a performance "
        "das operações transacionais do MySQL, o PeopleFlow utiliza um banco de dados NoSQL **MongoDB**. "
        "Os logs são armazenados na coleção `logs` e modelados como documentos BSON ricos com esquemas flexíveis "
        "adequados para três categorias principais de eventos:",
        body_style
    ))
    
    story.append(Paragraph("Logs de Operações CRUD (Tipo: cadastro, alteracao, exclusao)", h2_style))
    story.append(Paragraph(
        "Gerados na camada de serviços sempre que há inserção, modificação ou exclusão de dados cruciais. O documento armazena o "
        "estado completo do objeto persistido, servindo de rastros históricos em tempo real. Exemplo de documento JSON gravado no MongoDB:",
        body_style
    ))
    
    story.append(Paragraph(
        "{\n"
        "  \"_id\": ObjectId(\"66522c0e86b039474e0d9b4b\"),\n"
        "  \"timestamp\": ISODate(\"2026-05-25T16:15:30Z\"),\n"
        "  \"usuario\": \"admin@peopleflow.com\",\n"
        "  \"acao\": \"CREATE\",\n"
        "  \"tipo_evento\": \"cadastro\",\n"
        "  \"tabela\": \"employees\",\n"
        "  \"registro_id\": \"42\",\n"
        "  \"detalhes\": {\n"
        "    \"name\": \"Carlos Silva\",\n"
        "    \"email\": \"carlos.silva@peopleflow.com\",\n"
        "    \"position_id\": 2,\n"
        "    \"status\": \"ativo\"\n"
        "  },\n"
        "  \"ip\": \"172.18.0.1\",\n"
        "  \"user_agent\": \"Mozilla/5.0...\"\n"
        "}",
        code_style
    ))
    
    story.append(Paragraph("Logs de Acesso HTTP (Tipo: acesso_rota)", h2_style))
    story.append(Paragraph(
        "Gerados por um middleware de requisições (`app/middlewares/log_middleware.py`) que intercepta todas as requisições "
        "privadas e calcula o tempo gasto para o processamento da rota. Salva chaves como `endpoint`, `metodo` (GET, POST), "
        "`status_code` (200, 302, 404, 500) e `tempo_resposta` (medido em milissegundos).",
        body_style
    ))
    
    story.append(Paragraph("Logs de Exceções e Erros Críticos (Tipo: erro)", h2_style))
    story.append(Paragraph(
        "Interceptados centralizadamente por um middleware de exceções globais (`app/middlewares/error_middleware.py`). "
        "Quando ocorre um erro não previsto no backend (ex: Erro 500), o middleware captura o erro, monta o stack trace completo do Python "
        "via biblioteca <i>traceback</i>, e salva o log detalhado no MongoDB. Isso permite que a equipe técnica identifique a linha exata e a "
        "causa do erro sem expor informações confidenciais para o usuário final.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # --- PÁGINA 8: EXPORTAÇÃO XML ---
    story.append(Paragraph("8. Geração e Exportação de Logs no Formato XML", h1_style))
    story.append(Paragraph(
        "Para possibilitar a interoperabilidade com sistemas legados de governança corporativa e auditorias externas, o sistema "
        "desenvolveu um pipeline especializado em serializar as coleções dinâmicas do MongoDB em arquivos estruturados XML. "
        "Esta funcionalidade é implementada pelo <b>XmlService</b> (xml_service.py) e exposta no endpoint `/logs/export.xml`.",
        body_style
    ))
    story.append(Paragraph("Como Funciona a Serialização de Logs:", h2_style))
    story.append(Paragraph("1. O usuário acessa a rota no painel administrativo, aplicando opcionalmente filtros de e-mail, ação ou data.", list_style))
    story.append(Paragraph("2. A aplicação executa a busca parametrizada na coleção de logs do MongoDB, recuperando uma lista de objetos BSON ordenados por timestamp.", list_style))
    story.append(Paragraph("3. O XmlService cria o elemento raiz `<logs>` em memória usando a biblioteca padrão do Python <b>xml.etree.ElementTree</b>.", list_style))
    story.append(Paragraph("4. Para cada log, o serviço adiciona um nó filho `<evento>` contendo um atributo `id` de controle incremental.", list_style))
    story.append(Paragraph("5. Dados básicos do evento de auditoria são mapeados como sub-elementos textuais: `<usuario>`, `<acao>`, `<descricao>`, `<data_hora>`, `<tipo_evento>` e `<ip_origem>`.", list_style))
    story.append(Paragraph("6. Detalhes específicos de auditoria relacional são agrupados na tag aninhada `<dados_vinculados>`, contendo tags `<tabela>` e `<registro_id>`.", list_style))
    story.append(Paragraph("7. A árvore bruta é gerada e encaminhada para a biblioteca de controle de DOM <b>xml.dom.minidom</b>. "
                           "A biblioteca realiza a leitura em string (`parseString`) e executa o método `toprettyxml` com recuos de tabulação (indentações de 2 espaços) e declaração do charset UTF-8.", list_style))
    
    story.append(Spacer(1, 5))
    story.append(Paragraph("Exemplo de Formato XML Exportado pelo Sistema:", h2_style))
    story.append(Paragraph(
        "&lt;?xml version=\"1.0\" encoding=\"UTF-8\"?&gt;\n"
        "&lt;logs&gt;\n"
        "  &lt;evento id=\"1\"&gt;\n"
        "    &lt;usuario&gt;admin@peopleflow.com&lt;/usuario&gt;\n"
        "    &lt;acao&gt;CREATE&lt;/acao&gt;\n"
        "    &lt;descricao&gt;Ação de cadastro no banco de dados.&lt;/descricao&gt;\n"
        "    &lt;data_hora&gt;2026-05-25T16:15:30&lt;/data_hora&gt;\n"
        "    &lt;tipo_evento&gt;cadastro&lt;/tipo_evento&gt;\n"
        "    &lt;ip_origem&gt;172.18.0.1&lt;/ip_origem&gt;\n"
        "    &lt;dados_vinculados&gt;\n"
        "      &lt;tabela&gt;employees&lt;/tabela&gt;\n"
        "      &lt;registro_id&gt;42&lt;/registro_id&gt;\n"
        "    &lt;/dados_vinculados&gt;\n"
        "  &lt;/evento&gt;\n"
        "&lt;/logs&gt;",
        code_style
    ))
    
    story.append(PageBreak())
    
    # --- PÁGINA 9: RELATÓRIOS PDF E GRÁFICOS ---
    story.append(Paragraph("9. Explicação dos Relatórios Dinâmicos em PDF", h1_style))
    story.append(Paragraph(
        "A emissão de relatórios de pessoal em conformidade com as regras corporativas é uma exigência essencial. "
        "O PeopleFlow atende a essa exigência de forma nativa por meio da biblioteca **ReportLab**, amplamente consolidada "
        "para desenho de documentos em Python. A geração é executada pelo <b>PdfService</b> (pdf_service.py) e baixada via `/reports/employees/pdf`.",
        body_style
    ))
    
    story.append(Paragraph("Estrutura Física e Visual do PDF:", h2_style))
    story.append(Paragraph("• <b>Orientação Paisagem (Landscape A4):</b> Como a listagem de colaboradores exige várias colunas "
                           "(Nome, E-mail, Departamento, Cargo, Status, Data de Admissão), o arquivo é estruturado com o layout de página "
                           "rotacionado horizontalmente para evitar quebras abruptas de linhas nas colunas e garantir legibilidade ideal.", list_style))
    story.append(Paragraph("• <b>Desenho Dinâmico via Platypus:</b> O serviço utiliza a API de alto nível do ReportLab (Platypus) montando o documento "
                           "com fluxo de objetos sequenciais (`SimpleDocTemplate`), adicionando títulos, subtítulos, espaçadores (`Spacer`) e tabelas estruturadas.", list_style))
    story.append(Paragraph("• <b>Tabelas Estilizadas (TableStyle):</b> A tabela com a listagem dos dados dos colaboradores possui largura de colunas "
                           "definida de forma explícita (`[140, 190, 115, 130, 70, 80]`). O cabeçalho é colorido com a cor azul-escuro institucional (#263238) "
                           "e o corpo da tabela possui coloração zebrada (linhas alternadas entre branco e cinza-claro #F4F7F8) com grades de 0.4 pontos.", list_style))
    story.append(Paragraph("• <b>Totalizadores Gerenciais:</b> Ao término da tabela, o relatório processa os colaboradores ativos e inativos em memória, "
                           "adicionando dinamicamente um bloco destacado com a soma total do filtro ativo.", list_style))
    story.append(Paragraph("• <b>Rodapés Dinâmicos via Canvas:</b> Por meio de funções de callback (`onFirstPage` e `onLaterPages`), o sistema desenha "
                           "com o canvas nativo do ReportLab uma linha divisória, o copyright do PeopleFlow e a numeração da página (\"Página X\").", list_style))
    
    story.append(Paragraph("10. Painel de Indicadores e Gráfico (Chart.js)", h1_style))
    story.append(Paragraph(
        "Para a visualização rápida e apoio a decisões executivas, o painel de controle (Dashboard) renderiza um gráfico de barras "
        "interativo contendo o número total de colaboradores distribuídos por departamento.",
        body_style
    ))
    story.append(Paragraph("Detalhamento Técnico da Integração do Gráfico:", h2_style))
    story.append(Paragraph("• <b>Tecnologia Cliente-Side:</b> O gráfico é processado diretamente no navegador utilizando a biblioteca <b>Chart.js v4</b> carregada via CDN institucional.", list_style))
    story.append(Paragraph("• <b>Fonte de Dados Dinâmica (API RESTful):</b> Ao ser carregado, o script assíncrono `app/static/js/charts.js` realiza uma chamada HTTP assíncrona "
                           "(`fetch('/api/charts/employees-by-department')`) ao endpoint RESTful do backend.", list_style))
    story.append(Paragraph("• <b>Consulta Agregada do Backend:</b> A rota do backend aciona o <i>ChartService</i> que repassa a consulta agregada executada pelo <i>EmployeeDAO</i>. "
                           "A consulta realiza um agrupamento (`GROUP BY`) no MySQL unindo as tabelas `departments`, `positions` e `employees`, "
                           "e conta a quantidade de funcionários por departamento, convertendo a saída em uma estrutura de JSON mapeada:", list_style))
    story.append(Paragraph(
        "{\n"
        "  \"labels\": [\"Tecnologia\", \"RH\", \"Financeiro\", \"Vendas\"],\n"
        "  \"data\": [12, 4, 3, 7]\n"
        "}",
        code_style
    ))
    
    story.append(PageBreak())
    
    # --- PÁGINA 10: COMO EXECUTAR O PROJETO ---
    story.append(Paragraph("11. Como Executar o Projeto (Guia Passo a Passo)", h1_style))
    story.append(Paragraph(
        "O ambiente de execução da aplicação é totalmente conteinerizado utilizando o Docker e orquestrado via Docker Compose, "
        "eliminando problemas de compatibilidade e configurações manuais na máquina de testes.",
        body_style
    ))
    
    story.append(Paragraph("Etapa 1: Subir os Containers do Sistema", h2_style))
    story.append(Paragraph(
        "Abra o terminal na pasta raiz do projeto (onde está o arquivo `docker-compose.yml`) e execute o comando para construir e "
        "subir todos os serviços necessários em segundo plano:",
        body_style
    ))
    story.append(Paragraph("docker compose up --build -d", code_style))
    story.append(Paragraph(
        "Esse comando inicializa cinco containers:\n"
        "• <b>app:</b> Servidor web executando a aplicação Flask na porta 5000.\n"
        "• <b>db:</b> Banco de dados MySQL 8 de persistência relacional na porta 3306.\n"
        "• <b>mongodb:</b> Banco de dados NoSQL de logs na porta 27017.\n"
        "• <b>phpmyadmin:</b> Gerenciador visual web para o MySQL rodando na porta 8081.\n"
        "• <b>mongo-express:</b> Gerenciador visual web para o MongoDB rodando na porta 8082.",
        body_style
    ))
    
    story.append(Paragraph("Etapa 2: Inicializar as Migrações e Criar as Tabelas MySQL", h2_style))
    story.append(Paragraph(
        "Com os containers em execução, as tabelas relacionais do MySQL devem ser estruturadas. Isso é feito de forma automática "
        "aplicando as migrações geradas pelo Flask-Migrate (Alembic) de dentro do container:",
        body_style
    ))
    story.append(Paragraph(
        "docker compose exec app flask db init\n"
        "docker compose exec app flask db migrate -m \"initial tables\"\n"
        "docker compose exec app flask db upgrade",
        code_style
    ))
    
    story.append(Paragraph("Etapa 3: Popular o Banco de Dados com Dados de Teste (Seeds)", h2_style))
    story.append(Paragraph(
        "Para facilitar o teste do sistema, foi desenvolvido um comando CLI customizado do Flask (`flask seed`) que preenche "
        "os registros obrigatórios das tabelas do MySQL (Administrador inicial, Departamentos, Cargos e Competências básicas):",
        body_style
    ))
    story.append(Paragraph("docker compose exec app flask seed", code_style))
    
    story.append(Paragraph("Etapa 4: Acessar a Aplicação e Credenciais de Login", h2_style))
    story.append(Paragraph(
        "Com o banco populado, acesse o navegador de sua preferência e navegue nos seguintes endereços:\n"
        "• <b>Aplicação PeopleFlow:</b> <a href=\"http://localhost:5000\">http://localhost:5000</a>\n"
        "• <b>Gerenciamento de Bancos MySQL:</b> <a href=\"http://localhost:8081\">http://localhost:8081</a>\n"
        "• <b>Gerenciamento de Logs MongoDB:</b> <a href=\"http://localhost:8082\">http://localhost:8082</a>\n\n"
        "<b>Credenciais de Acesso Administrativo Inicial:</b>\n"
        "• <b>E-mail:</b> <font face=\"Courier\">admin@peopleflow.com</font> | <b>Senha:</b> <font face=\"Courier\">admin123</font>",
        body_style
    ))
    
    story.append(PageBreak())
    
    # --- PÁGINAS 11 E 12: LISTA DE ENDPOINTS DA API ---
    story.append(Paragraph("12. Lista Completa de Endpoints e Rotas da API", h1_style))
    story.append(Paragraph(
        "A tabela a seguir descreve de forma minuciosa todas as rotas de navegação administrativa, APIs RESTful de gráficos e exportações, "
        "e endpoints de controle de sessão da aplicação PeopleFlow.",
        body_style
    ))
    
    # Tabela com lista completa de endpoints
    endpoints_data = [
        [Paragraph("<b>Rota / Endpoint</b>", table_header), Paragraph("<b>Met.</b>", table_header), Paragraph("<b>Controlador / Ação</b>", table_header), Paragraph("<b>Descrição / Acesso</b>", table_header)],
        
        # Sessão e Autenticação
        [Paragraph("/login", table_text), Paragraph("GET<br/>POST", table_text), Paragraph("AuthController.login<br/>AuthController.authenticate", table_text), Paragraph("Renderiza tela de login e processa a autenticação do administrador.", table_text)],
        [Paragraph("/register", table_text), Paragraph("GET<br/>POST", table_text), Paragraph("AuthController.register<br/>AuthController.store", table_text), Paragraph("Renderiza formulário de cadastro de administradores e persiste no MySQL.", table_text)],
        [Paragraph("/logout", table_text), Paragraph("GET<br/>POST", table_text), Paragraph("AuthController.logout", table_text), Paragraph("Finaliza a sessão do administrador ativo e redireciona ao login.", table_text)],
        
        # Dashboard
        [Paragraph("/dashboard", table_text), Paragraph("GET", table_text), Paragraph("DashboardController.index", table_text), Paragraph("<b>Privada.</b> Exibe painel principal com estatísticas consolidadas e gráfico.", table_text)],
        
        # CRUD Colaboradores
        [Paragraph("/employees", table_text), Paragraph("GET", table_text), Paragraph("EmployeeController.index", table_text), Paragraph("<b>Privada.</b> Exibe listagem zebrada de colaboradores com filtros ativos.", table_text)],
        [Paragraph("/employees/&lt;id&gt;", table_text), Paragraph("GET", table_text), Paragraph("EmployeeController.show", table_text), Paragraph("<b>Privada.</b> Exibe ficha detalhada e competências de um colaborador.", table_text)],
        [Paragraph("/employees/create", table_text), Paragraph("GET", table_text), Paragraph("EmployeeController.create", table_text), Paragraph("<b>Privada.</b> Exibe tela para criação de novo colaborador com checkbox de habilidades.", table_text)],
        [Paragraph("/employees", table_text), Paragraph("POST", table_text), Paragraph("EmployeeController.store", table_text), Paragraph("<b>Privada.</b> Processa o formulário de cadastro, salva foto UUID e insere no MySQL.", table_text)],
        [Paragraph("/employees/&lt;id&gt;/edit", table_text), Paragraph("GET", table_text), Paragraph("EmployeeController.edit", table_text), Paragraph("<b>Privada.</b> Exibe formulário preenchido de edição do colaborador correspondente.", table_text)],
        [Paragraph("/employees/&lt;id&gt;/update", table_text), Paragraph("POST", table_text), Paragraph("EmployeeController.update", table_text), Paragraph("<b>Privada.</b> Processa formulário de atualização e persiste modificações no MySQL.", table_text)],
        [Paragraph("/employees/&lt;id&gt;/delete", table_text), Paragraph("POST", table_text), Paragraph("EmployeeController.destroy", table_text), Paragraph("<b>Privada.</b> Exclui colaborador do MySQL, remove vínculos de habilidades e loga.", table_text)],
        
        # CRUD Departamentos
        [Paragraph("/departments", table_text), Paragraph("GET<br/>POST", table_text), Paragraph("DepartmentController.index<br/>DepartmentController.store", table_text), Paragraph("<b>Privada.</b> Lista departamentos e processa criação de novos departamentos.", table_text)],
        [Paragraph("/departments/&lt;id&gt;/update", table_text), Paragraph("POST", table_text), Paragraph("DepartmentController.update", table_text), Paragraph("<b>Privada.</b> Atualiza nome e descrição do departamento.", table_text)],
        [Paragraph("/departments/&lt;id&gt;/delete", table_text), Paragraph("POST", table_text), Paragraph("DepartmentController.destroy", table_text), Paragraph("<b>Privada.</b> Exclui departamento se não houver cargos vinculados a ele.", table_text)],
        
        # CRUD Cargos
        [Paragraph("/positions", table_text), Paragraph("GET<br/>POST", table_text), Paragraph("PositionController.index<br/>PositionController.store", table_text), Paragraph("<b>Privada.</b> Lista os cargos disponíveis por departamento e insere novos.", table_text)],
        [Paragraph("/positions/&lt;id&gt;/update", table_text), Paragraph("POST", table_text), Paragraph("PositionController.update", table_text), Paragraph("<b>Privada.</b> Altera dados cadastrais de cargo cadastrado.", table_text)],
        [Paragraph("/positions/&lt;id&gt;/delete", table_text), Paragraph("POST", table_text), Paragraph("PositionController.destroy", table_text), Paragraph("<b>Privada.</b> Exclui cargo caso não existam colaboradores alocados.", table_text)],
        
        # CRUD Competências
        [Paragraph("/skills", table_text), Paragraph("GET<br/>POST", table_text), Paragraph("SkillController.index<br/>SkillController.store", table_text), Paragraph("<b>Privada.</b> Lista e cadastra competências aplicáveis a colaboradores.", table_text)],
        [Paragraph("/skills/&lt;id&gt;/update", table_text), Paragraph("POST", table_text), Paragraph("SkillController.update", table_text), Paragraph("<b>Privada.</b> Modifica nome de habilidade.", table_text)],
        [Paragraph("/skills/&lt;id&gt;/delete", table_text), Paragraph("POST", table_text), Paragraph("SkillController.destroy", table_text), Paragraph("<b>Privada.</b> Remove habilidade se não possuir colaboradores vinculados.", table_text)],
        
        # Integrações, Exportações e Relatórios
        [Paragraph("/logs", table_text), Paragraph("GET", table_text), Paragraph("LogController.index", table_text), Paragraph("<b>Privada.</b> Exibe painel de logs de auditoria recuperados do MongoDB.", table_text)],
        [Paragraph("/logs/export.xml", table_text), Paragraph("GET", table_text), Paragraph("LogController.export_xml", table_text), Paragraph("<b>Privada.</b> Gera e faz download de logs serializados no formato de árvore XML.", table_text)],
        [Paragraph("/reports/employees", table_text), Paragraph("GET", table_text), Paragraph("ReportController.index", table_text), Paragraph("<b>Privada.</b> Exibe visualizador de relatórios com filtros avançados.", table_text)],
        [Paragraph("/reports/employees/pdf", table_text), Paragraph("GET", table_text), Paragraph("ReportController.export_pdf", table_text), Paragraph("<b>Privada.</b> Compila o relatório em ReportLab e baixa o PDF Landscape.", table_text)],
        
        # JSON Import/Export
        [Paragraph("/imports", table_text), Paragraph("GET", table_text), Paragraph("JsonController.index", table_text), Paragraph("<b>Privada.</b> Apresenta tela para upload de arquivos JSON de importação.", table_text)],
        [Paragraph("/imports/&lt;entity&gt;", table_text), Paragraph("POST", table_text), Paragraph("JsonController.import_&lt;entity&gt;", table_text), Paragraph("<b>Privada.</b> Processa upload de JSON e persiste em lote no MySQL.", table_text)],
        [Paragraph("/exports/&lt;entity&gt;.json", table_text), Paragraph("GET", table_text), Paragraph("JsonController.export_&lt;entity&gt;", table_text), Paragraph("<b>Privada.</b> Serializa tabela do MySQL em arquivo JSON legível para download.", table_text)],
        
        # API de Gráficos (REST JSON)
        [Paragraph("/api/charts/employees-by-department", table_text), Paragraph("GET", table_text), Paragraph("ChartController.employees_by_department", table_text), Paragraph("<b>Privada (REST API).</b> Fornece rótulos e somas para renderização do Chart.js.", table_text)]
    ]
    
    endpoints_table = Table(endpoints_data, colWidths=[120, 35, 140, 192])
    endpoints_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    story.append(endpoints_table)
    
    # Construção do Documento usando o NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF de Documentação técnica gerado com sucesso!")

if __name__ == "__main__":
    build_pdf()
