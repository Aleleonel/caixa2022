-- MySQL dump 10.13  Distrib 5.7.33, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: controle_clientes
-- ------------------------------------------------------
-- Server version	5.7.33-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `caixa`
--

DROP TABLE IF EXISTS `caixa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `caixa` (
  `idcaixa` int(11) NOT NULL AUTO_INCREMENT,
  `nr_caixa` int(11) NOT NULL,
  `id_produtos` int(11) DEFAULT NULL,
  `id_vendedor` int(11) DEFAULT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `quantidade` int(11) DEFAULT NULL,
  `valor_total` decimal(10,2) DEFAULT NULL,
  `ultupdate` date DEFAULT NULL,
  PRIMARY KEY (`idcaixa`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `caixa`
--

LOCK TABLES `caixa` WRITE;
/*!40000 ALTER TABLE `caixa` DISABLE KEYS */;
INSERT INTO `caixa` VALUES (1,1,12,1,14,2,31.98,'2021-04-13'),(24,2,13,1,1,50,2250.00,'2021-04-14');
/*!40000 ALTER TABLE `caixa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cidades`
--

DROP TABLE IF EXISTS `cidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cidades` (
  `idcidades` int(11) NOT NULL AUTO_INCREMENT,
  `cidades` varchar(45) DEFAULT NULL,
  `uf` varchar(2) DEFAULT NULL,
  `ultupdate` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idcidades`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cidades`
--

LOCK TABLES `cidades` WRITE;
/*!40000 ALTER TABLE `cidades` DISABLE KEYS */;
/*!40000 ALTER TABLE `cidades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clientes` (
  `codigo` int(11) NOT NULL AUTO_INCREMENT,
  `tipo` varchar(15) DEFAULT NULL,
  `nome` varchar(60) DEFAULT NULL,
  `cpf` varchar(20) DEFAULT NULL,
  `rg` varchar(20) DEFAULT NULL,
  `telefone` varchar(15) DEFAULT NULL,
  `endereco` varchar(100) DEFAULT NULL,
  `idcidade` int(11) DEFAULT NULL,
  `ultupdate` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'pessoa Física','Alexandre Leonel de Oliveira','25664097817','287752537','11971512237','Rua Ernestina Loschi, 76',NULL,'2021-04-04 15:58:30'),(2,'Pessoa Jurídica','Rosemary A. de Oliveira','13592883844','18802072','11975618992','Rua Ernestina Loschi, 76',NULL,'2021-04-04 15:58:30'),(12,'Pessoa Física','Iara Cristina do Carmo Mina','25667097817','287752537','11971512237','Rua João Scabin 409',NULL,'2021-04-04 15:58:30'),(13,'Pessoa Física','Clovis Fagunde Junior','25667097817','287752537','11971512237','Rua Petronílha Antunes 58',NULL,'2021-04-04 15:58:30'),(14,'Pessoa Física','Bigo Rilho','25664097817','287752537','11971512237','Rua 23 de Maio 45',NULL,'2021-04-04 15:58:30'),(15,'Pessoa Física','Marley Camargo','25664097817','287752537','11971512237','Rua Rio branco 123',NULL,'2021-04-04 15:58:30'),(16,'Pessoa Física','Sonia Regina do Carmo Mina','25664097817','287752537','11971512237','Rua ponte torta 345',NULL,'2021-04-04 15:58:30'),(17,'Pessoa Física','Luna Cachorrinha','12005487457','78457788773','11971512237','Rua ernestina loschi 76',NULL,'2021-04-04 15:58:30'),(18,'Pessoa Física','Kiko cachorrinho chato','12356897487','457845781112','1175618992','Rua Do Cruzeiro 85',NULL,'2021-04-04 15:58:30');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estoque`
--

DROP TABLE IF EXISTS `estoque`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estoque` (
  `idproduto` int(11) NOT NULL,
  `estoque` decimal(10,0) DEFAULT '0',
  `ultupdate` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` varchar(1) NOT NULL,
  PRIMARY KEY (`idproduto`),
  CONSTRAINT `fk_estoque_produtos` FOREIGN KEY (`idproduto`) REFERENCES `produtos` (`codigo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoque`
--

LOCK TABLES `estoque` WRITE;
/*!40000 ALTER TABLE `estoque` DISABLE KEYS */;
INSERT INTO `estoque` VALUES (2,100,'2021-04-05 14:15:45','E'),(3,100,'2021-04-05 14:15:45','E'),(5,100,'2021-04-05 14:15:45','E'),(6,200,'2021-04-05 19:13:53','E'),(8,500,'2021-04-05 19:14:36','E'),(9,250,'2021-04-05 19:27:25','E'),(10,500,'2021-04-05 19:28:46','E'),(11,40,'2021-04-05 19:32:56','E'),(12,600,'2021-04-05 19:36:53','E'),(13,300,'2021-04-05 19:39:46','E'),(14,350,'2021-04-05 21:02:39','E'),(15,350,'2021-04-05 21:20:46','E'),(16,60,'2021-04-06 01:00:10','E'),(17,100,'2021-04-06 02:50:26','E');
/*!40000 ALTER TABLE `estoque` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidocaixa`
--

DROP TABLE IF EXISTS `pedidocaixa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pedidocaixa` (
  `idpedidocaixa` int(11) NOT NULL AUTO_INCREMENT,
  `nr_caixa` int(11) DEFAULT NULL,
  `cod_produto` int(11) DEFAULT NULL,
  `cod_vendedor` int(11) DEFAULT NULL,
  `cod_cliente` int(11) DEFAULT NULL,
  `quantidade` int(11) DEFAULT NULL,
  `valor_total` decimal(10,2) DEFAULT NULL,
  `ultupdate` date DEFAULT NULL,
  PRIMARY KEY (`idpedidocaixa`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidocaixa`
--

LOCK TABLES `pedidocaixa` WRITE;
/*!40000 ALTER TABLE `pedidocaixa` DISABLE KEYS */;
INSERT INTO `pedidocaixa` VALUES (1,1,2,1,1,1,22.60,'2021-04-13'),(2,2,13,1,1,4,180.00,'2021-04-14'),(3,2,13,1,2,1,45.00,'2021-04-14'),(4,2,16,1,2,1,14.50,'2021-04-14'),(5,2,17,1,2,2,6.00,'2021-04-14'),(6,2,2,1,2,2,50.70,'2021-04-14'),(7,2,14,1,16,2,59.80,'2021-04-14'),(10,2,16,1,1,1,14.50,'2021-04-14');
/*!40000 ALTER TABLE `pedidocaixa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `precos`
--

DROP TABLE IF EXISTS `precos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `precos` (
  `idprecos` int(11) NOT NULL,
  `preco` decimal(15,2) DEFAULT NULL,
  `ultupdate` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idprecos`),
  CONSTRAINT `fk_precos_produtos` FOREIGN KEY (`idprecos`) REFERENCES `produtos` (`codigo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `precos`
--

LOCK TABLES `precos` WRITE;
/*!40000 ALTER TABLE `precos` DISABLE KEYS */;
INSERT INTO `precos` VALUES (2,19.00,'2021-04-04 14:04:42'),(3,100.00,'2021-04-04 14:07:59'),(5,150.00,'2021-04-04 14:08:51'),(6,30.00,'2021-04-06 00:50:00'),(8,30.99,'2021-04-06 00:50:00'),(9,50.00,'2021-04-06 00:50:00'),(10,15.65,'2021-04-06 00:50:00'),(11,5.90,'2021-04-06 00:50:00'),(12,16.00,'2021-04-06 00:50:00'),(13,45.00,'2021-04-06 00:50:00'),(14,19.99,'2021-04-05 21:02:39'),(15,30.00,'2021-04-06 00:50:00'),(16,23.50,'2021-04-06 01:00:10'),(17,1.50,'2021-04-06 02:50:26');
/*!40000 ALTER TABLE `precos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produtos` (
  `codigo` int(11) NOT NULL AUTO_INCREMENT,
  `descricao` varchar(60) DEFAULT NULL,
  `ncm` varchar(20) DEFAULT NULL,
  `un` varchar(2) DEFAULT NULL,
  `preco` decimal(15,2) DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
INSERT INTO `produtos` VALUES (2,'ESMALTE VERMELHO','156457897487','UN',25.35),(3,'LENÇOS UMEDECIDOS','745121245789863636','CX',3.99),(5,'MASCARA FACIAL','12454545777777','UN',19.90),(6,'PÓ DE ARROZ','123456667899','UN',51.99),(8,'PROTETOR LABIAL','031245678999958','UN',2.00),(9,'MASCARA PARA CÍLIOS','03124578','UN',58.99),(10,'HIDRATANTE PARA O CORPO','12356899887878','UN',6.90),(11,'PRIMER','0124585236547','UN',60.85),(12,'LIXA PARA PÉS CASCUDOS','66688875451122','UN',15.99),(13,'ALICATE DE CUTÍCULA','1212124545488999','UN',45.00),(14,'HIMEL','7845789988855','UN',29.90),(15,'BATON VERMELHO','1255544487888','UN',23.90),(16,'ALGODÃO','12457898745787','UN',14.50),(17,'ACETONA','14577887788','UN',3.00);
/*!40000 ALTER TABLE `produtos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `idusuarios` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(16) NOT NULL,
  `senha` varchar(8) NOT NULL,
  `dt_nascimento` date DEFAULT NULL,
  `ultupdate` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idusuarios`),
  UNIQUE KEY `usuario_senha_UNIQUE` (`senha`),
  UNIQUE KEY `usuario_nome_UNIQUE` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Alexandre','03120808','1974-06-26','2021-04-06 14:04:42'),(2,'Rose','252666','1966-12-25','2021-04-06 22:58:42');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendas`
--

DROP TABLE IF EXISTS `vendas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vendas` (
  `idvendas` int(11) NOT NULL AUTO_INCREMENT,
  `id_produto` int(11) DEFAULT NULL,
  `id_caixa` int(11) DEFAULT NULL,
  `id_vendedor` int(11) DEFAULT NULL,
  PRIMARY KEY (`idvendas`),
  KEY `fk_vendas_produtos_idx` (`id_produto`),
  KEY `fk_vendas_caixa_idx` (`id_caixa`),
  KEY `fk_vendas_vendedor_idx` (`id_vendedor`),
  CONSTRAINT `fk_vendas_caixa` FOREIGN KEY (`id_caixa`) REFERENCES `caixa` (`idcaixa`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_vendas_produtos` FOREIGN KEY (`id_produto`) REFERENCES `produtos` (`codigo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_vendas_vendedor` FOREIGN KEY (`id_vendedor`) REFERENCES `vendedores` (`idvendedores`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendas`
--

LOCK TABLES `vendas` WRITE;
/*!40000 ALTER TABLE `vendas` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendedores`
--

DROP TABLE IF EXISTS `vendedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vendedores` (
  `idvendedores` int(11) NOT NULL AUTO_INCREMENT,
  `vendedor` varchar(45) DEFAULT NULL,
  `cpf` varchar(45) DEFAULT NULL,
  `ultupdate` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`idvendedores`),
  UNIQUE KEY `cpf_UNIQUE` (`cpf`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendedores`
--

LOCK TABLES `vendedores` WRITE;
/*!40000 ALTER TABLE `vendedores` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'controle_clientes'
--

--
-- Dumping routines for database 'controle_clientes'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-15 18:05:41
