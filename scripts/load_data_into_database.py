#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb

talbe_dir = '/home/ming/macaca/snvs/tables/'

conn = MySQLdb.connect(
	host = 'localhost',
	port = 3306,
	user = 'root',
	passwd = 'du920128',
	db = 'macaca'
)
c = conn.cursor()

#prefix = 'macaca'

"""
variant_sql = '''
CREATE TABLE IF NOT EXISTS variant{0} (
	id int(11) NOT NULL AUTO_INCREMENT,
	genotype tinyint(1) NOT NULL,
	chromosome_id int(11) NOT NULL,
	individual_id int(11) NOT NULL,
	snp_id int(11) NOT NULL,
	PRIMARY KEY (id),
	KEY variant_genotype_{0} (genotype),
	KEY variant_individual_{0} (individual_id),
	KEY variant_snp_{0} (snp_id),
	KEY variant_genotype_individual_{0} (genotype,individual_id),
	KEY variant_genotype_snp_{0} (genotype,snp_id),
	KEY variant_individual_snp_{0} (individual_id,snp_id),
	KEY variant_genotype_individual_snp_{0} (genotype,individual_id,snp_id)
) ENGINE=Aria DEFAULT CHARSET=utf8
'''

snp_sql = '''
CREATE TABLE IF NOT EXISTS snp{0} (
	id int(11) NOT NULL AUTO_INCREMENT,
	snp_id int(11) NOT NULL,
	position int(11) NOT NULL,
	chromosome_id int(11) NOT NULL,
	PRIMARY KEY (id),
	KEY snp_snp_id_{0} (snp_id),
	KEY snp_position_{0} (position),
	KEY snp_chromosome_id_{0} (chromosome_id),
	KEY snp_position_chromosome_id_{0} (position, chromosome_id),
	KEY snp_snp_chromosome_id_{0} (snp_id, chromosome_id)
) ENGINE=Aria DEFAULT CHARSET=utf8
'''

non_sql = '''
CREATE TABLE IF NOT EXISTS nonvariant{0} (
	id int(11) NOT NULL AUTO_INCREMENT,
	individual_id int(11) NOT NULL,
	snp_id int(11) NOT NULL,
	PRIMARY KEY (id),
	KEY non_individual_id_{0} (individual_id),
	KEY non_snp_id_{0} (snp_id),
	KEY non_indivdual_snp_{0} (individual_id, snp_id)
) ENGINE=Aria DEFAULT CHARSET=utf8
'''

for i in range(1, 21):
	c.execute(variant_sql.format(i))
	c.execute(snp_sql.format(i))
	c.execute(non_sql.format(i))
"""

print('load base information')

c.execute("delete from chromosome")
c.execute("delete from groups")
c.execute("delete from species")
c.execute("delete from individual")
c.execute("delete from gene")
c.execute("delete from transcript")
c.execute("delete from gannot")
c.execute("delete from tannot")
c.execute("delete from mutation")
c.execute("delete from function")
c.execute("delete from funcannot")
c.execute("delete from disease")
c.execute("delete from drug")
c.execute("delete from orthology")

c.execute("load data local infile '{}chromosome.table' into table chromosome fields terminated by '\t'".format(talbe_dir))
c.execute("load data local infile '{}group.table' into table groups fields terminated by '\t'".format(talbe_dir))
c.execute("load data local infile '{}species.table' into table species fields terminated by '\t'".format(talbe_dir))
c.execute("load data local infile '{}individual.table' into table individual fields terminated by '\t'".format(talbe_dir))
c.execute("load data local infile '{}gene.table' into table gene fields terminated by '\t'".format(talbe_dir))
c.execute("load data local infile '{}transcript.table' into table transcript fields terminated by '\t'".format(talbe_dir))
c.execute("load data local infile '{}gene_annot.table' into table gannot fields terminated by '\t'".format(talbe_dir))
c.execute("load data local infile '{}transcript_annot.table' into table tannot fields terminated by '\t'".format(talbe_dir))
c.execute("load data local infile '{}mutation.table' into table mutation fields terminated by '\t'".format(talbe_dir))
c.execute("load data local infile '{}function.table' into table function fields terminated by '\t'".format(talbe_dir))
c.execute("load data local infile '{}funcannot.table' into table funcannot fields terminated by '\t'".format(talbe_dir))
c.execute("load data local infile '{}disease.table' into table disease fields terminated by '\t'".format(talbe_dir))
c.execute("load data local infile '{}drug.table' into table drug fields terminated by '\t'".format(talbe_dir))
c.execute("load data local infile '{}orthology.table' into table orthology fields terminated by '\t'".format(talbe_dir))
#c.execute("load data local infile '{}statistics.table' into table statistics fields terminated by '\t'".format(talbe_dir))
print('load specific snps')
c.execute("delete from group_specific")
c.execute("delete from species_specific")
c.execute("load data local infile '{}group_specific.table' into table group_specific".format(talbe_dir))
c.execute("load data local infile '{}species_specific.table' into table species_specific".format(talbe_dir))
print('load snps')
c.execute("delete from snp")
c.execute("load data local infile '{}snp.table' into table snp".format(talbe_dir))
print('load variants')

#for i in range(1, 21):
#	c.execute("load data local infile 'snp.table.{0}' into table snp_{0}".format(i))

for i in range(1, 21):
	print('load variant, {0}'.format(i))
	c.execute("delete from variant{}".format(i))
	c.execute("load data local infile '{1}variant.table.{0}' into table variant{0}".format(i, talbe_dir))

for j in range(1, 21):
	print('load snps, {}'.format(j))
	c.execute("delete from snp{}".format(j))
	c.execute("load data local infile '{1}snp.table.{0}' into table snp{0}".format(j, talbe_dir))

for k in range(1, 21):
	print('load non, {}'.format(k))
	c.execute("delete from nonvariant{}".format(k))
	c.execute("load data local infile '{1}non_variant.table.{0}' into table nonvariant{0}".format(k, talbe_dir))

c.close()
conn.commit()
conn.close()
