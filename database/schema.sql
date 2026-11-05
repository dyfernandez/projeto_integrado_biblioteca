-- public.autor definition
-- Drop table
-- DROP TABLE public.autor;

create table public.autor ( id_autor int4 generated always as identity( increment by 1 minvalue 1 maxvalue 2147483647 start 1 cache 1 no cycle) not null,
nome_autor varchar(150) not null,
pais varchar(60) not null,
constraint autor_id_autor_not_null not null id_autor,
constraint autor_nome_autor_not_null not null nome_autor,
constraint autor_pais_not_null not null pais,
constraint newtable_pk primary key (id_autor));
-- public.livro definition
-- Drop table
-- DROP TABLE public.livro;

create table public.livro ( id_livro int4 generated always as identity( increment by 1 minvalue 1 maxvalue 2147483647 start 1 cache 1 no cycle) not null,
nome_livro varchar(200) not null,
ano_publicacao int4 not null,
copias int4 not null,
constraint livro_ano_publicacao_not_null not null ano_publicacao,
constraint livro_copias_nao_negativo check ((copias >= 0)),
constraint livro_copias_not_null not null copias,
constraint livro_id_livro_not_null not null id_livro,
constraint livro_nome_livro_not_null not null nome_livro,
constraint livro_pk primary key (id_livro));
-- public.usuario definition
-- Drop table
-- DROP TABLE public.usuario;

create table public.usuario ( id_usuario int4 generated always as identity( increment by 1 minvalue 1 maxvalue 2147483647 start 1 cache 1 no cycle) not null,
nome_usuario varchar(150) not null,
telefone varchar(20) not null,
email varchar(255) not null,
rua varchar(150) not null,
numero varchar(10) not null,
bairro varchar(100) not null,
constraint usuario_bairro_not_null not null bairro,
constraint usuario_email_not_null not null email,
constraint usuario_id_usuario_not_null not null id_usuario,
constraint usuario_nome_usuario_not_null not null nome_usuario,
constraint usuario_numero_not_null not null numero,
constraint usuario_pk primary key (id_usuario),
constraint usuario_rua_not_null not null rua,
constraint usuario_telefone_not_null not null telefone);
-- public.emprestimo definition
-- Drop table
-- DROP TABLE public.emprestimo;

create table public.emprestimo ( id_emprestimo int4 generated always as identity( increment by 1 minvalue 1 maxvalue 2147483647 start 1 cache 1 no cycle) not null,
id_usuario int4 not null,
id_livro int4 not null,
data_retirada date not null,
data_prev_devol date not null,
data_devol date null,
constraint emprestimo_id_livro_not_null not null id_livro,
constraint emprestimos_data_prev_devol_not_null not null data_prev_devol,
constraint emprestimos_data_retirada_not_null not null data_retirada,
constraint emprestimos_id_emprestimos_not_null not null id_emprestimo,
constraint emprestimos_id_usuario_not_null not null id_usuario,
constraint emprestimos_pk primary key (id_emprestimo),
constraint emprestimos_livro_fk foreign key (id_livro) references public.livro(id_livro),
constraint emprestimos_usuario_fk foreign key (id_usuario) references public.usuario(id_usuario));
-- public.livro_autor definition
-- Drop table
-- DROP TABLE public.livro_autor;

create table public.livro_autor ( id_livro_autor int4 generated always as identity( increment by 1 minvalue 1 maxvalue 2147483647 start 1 cache 1 no cycle) not null,
id_livro int4 not null,
id_autor int4 not null,
constraint livro_autor_id_autor_not_null not null id_autor,
constraint livro_autor_id_livro_autor_not_null not null id_livro_autor,
constraint livro_autor_id_livro_not_null not null id_livro,
constraint livro_autor_pk primary key (id_livro_autor),
constraint livro_autor_autor_fk foreign key (id_autor) references public.autor(id_autor),
constraint livro_autor_livro_fk foreign key (id_livro) references public.livro(id_livro));
