import boto3
import os, json, logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

glue_client = boto3.client('glue')
s3_client = boto3.client('s3')
    
glue_database_name = os.environ['GLUE_DATABASE_NAME']
s3_final_tables_bucket = os.environ['BUCKET_NAME']

def lambda_handler(event, context):

    response = glue_client.get_tables(DatabaseName=glue_database_name)

    ''' In Case NextToken is required
    
    if 'NextToken' in response.keys():
            while 'NextToken' in response.keys():
                tables = glue_client.get_tables(nextToken=response['NextToken'])

                for table in tables:
            
                    # Head of file
                    final_md_string = table['Name'] + "\n"
                    final_md_string += "=" * len(table['Name'])
                    final_md_string += "\n\n"
            
                    # Table Head
                    final_md_string += "|Nr|Datenfeldbezeichnung|Datentyp|Personengruppe|Verwendungszweck|Nutzungsdauer und Loeschung|\n"
                    final_md_string += "| :---: | :---: | :---: | :---: | :---: | :---: |\n"
            
                    # Table Contents
                    for index, column in enumerate(table['StorageDescriptor']['Columns']):
                        final_md_string += "|{}|{}|{}|{}|{}|{}|\n".format(index, column['Name'], column['Type'], "keine", "-", "")
            
                    logger.error(final_md_string)
                    uploadMdFile(table['Name'], final_md_string, s3_final_tables_bucket, glue_database_name + '/' + table['Name'] + '.md')
    else:
    '''
    
    for table in response['TableList']:
        
        # Table Name Header
        final_md_string = table['Name'] + "\n"
        final_md_string += "=" * len(table['Name'])
        final_md_string += "\n\n"
        
        # Table Head
        final_md_string += "|Nr|Datenfeldbezeichnung|Datentyp|Personengruppe|Verwendungszweck|Nutzungsdauer und Loeschung|\n"
        final_md_string += "| :---: | :---: | :---: | :---: | :---: | :---: |\n"
        
        # Table Rows
        for index, column in enumerate(table['StorageDescriptor']['Columns']):
            final_md_string += "|{}|{}|{}|{}|{}|{}|\n".format(index, column['Name'], column['Type'], "keine", "-", "")
        
        logger.debug(final_md_string)
        uploadMdFile(table['Name'], final_md_string, s3_final_tables_bucket, glue_database_name + '/' + table['Name'] + '.md')


def uploadMdFile(fileName, md_string, bucketname, bucketkey):
    
    filepath = '/tmp/{}.md'.format(fileName)
    
    logger.debug("Writing Markdown to file: {}".format(fileName))
    with open(filepath, "w") as f:
        f.write(md_string)
    
    logger.debug("Uploading Markdown to S3: {}".format(fileName))
    md_binary = open(filepath, 'rb').read()
    return_s3_upload = s3_client.put_object(ACL='bucket-owner-read',Body=md_binary, ContentType='text/markdown', Bucket=bucketname, Key=bucketkey)
    logger.info("s3_client.put_object - bucketname: {}, bucketkey: {}".format(bucketname,bucketkey))
    return True