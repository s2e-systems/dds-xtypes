
#include <dds/dds.hh>
#include <dds/dds_typesupport.hh>
#include <dds/xtypes.hh>
#include <dds/xtypes_dtype.h>

#define DDS_BOOLEAN_TRUE         (1)
#define DDS_BOOLEAN_FALSE        (0)
#define LISTENER_STATUS_MASK_ALL (ALL_STATUS)

#define CONFIGURE_PARTICIPANT_FACTORY config_dpf();

void StringSeq_push(DDS::StringSeq  &string_seq, const char *elem)
{
  char * e = NULL;
  if ( elem )
    {
      e = new char[strlen(elem)+1];
      if ( e )
        {
          strcpy( e, elem );
          string_seq.push_back(e);
        }
    }
}

const char *get_qos_policy_name(DDS_QosPolicyId_t policy_id)
{
  return DDS_qos_policy_str(policy_id);
}

void
config_dpf()
{
  /* Some tests require us to allow assignment that would reduce the fidelity of a key field.
   * Our default is not to allow this, but it is configurable.
   * Until we resolve some ambiguity/interpretation in the spec, we will need this option to
   * pass these tests:
   *  - xtypes_v2_struct_test_suite_struct_key_string_3 
   *  - xtypes_v2_struct_test_suite_struct_key_enum_2 
   *  - xtypes_v2_struct_test_suite_struct_key_seq_2
   */
  setenv( "COREDX_ALLOW_LOSSY_KEY", "1", 1 );
}


DDS::TypeConsistencyEnforcementQosPolicy
TypeConsistency_get_default(void) {
  DDS::TypeConsistencyEnforcementQosPolicy rval;
  DDS::DomainParticipantFactory *dpf =  DDS::DomainParticipantFactory::get_instance();
  if ( dpf )
    {
      DDS::DomainParticipantFactoryQos dpf_qos;
      dpf->get_qos( dpf_qos );
      dpf_qos.entity_factory.autoenable_created_entities = 0;
      dpf->set_qos( dpf_qos );
  
      DDS::DomainParticipant * dp = dpf->create_participant( 0, DDS::PARTICIPANT_QOS_DEFAULT, NULL, 0 );
      if ( dp )
        {
          DDS::Subscriber * sub = dp->create_subscriber( DDS::SUBSCRIBER_QOS_DEFAULT, NULL, 0 );
          DDS::DataReaderQos dr_qos;
          sub->get_default_datareader_qos( dr_qos );
          rval = dr_qos.type_consistency;  
          dp->delete_contained_entities( );
          dpf->delete_participant( dp );
        }
      dpf->get_qos( dpf_qos );
      dpf_qos.entity_factory.autoenable_created_entities = 1;
      dpf->set_qos( dpf_qos );
    }
  return rval;
}

void disable_type_information(DDS::DomainParticipantQos &dp_qos)
{
  /* TODO: has to be done at reader/writer qos */
}

void set_type_object_version(DDS::DomainParticipantQos &dp_qos, int version)
{
#if (COREDX_DDS_VERSION_MAJOR >= 6)
  if (version == 1) {
    dp_qos.discovery.send_typeobj_v1 = 1;
    dp_qos.discovery.send_typeobj_v2 = 0;
  } else if (version == 2) {
    dp_qos.discovery.send_typeobj_v1 = 0;
    dp_qos.discovery.send_typeobj_v2 = 1;
  } else {
    std::cerr << "Unsupported Type Object version: " << version
              << ". Using default." << std::endl;
  }
#else
  /* TODO: has to be done at reader/writer qos */
#endif
}

DDS::DynamicType  *
create_type( DDS::DomainParticipant * dp,
             const char * type_folder,
             const char * type_file,
             const char * type_name )
{
  DDS::DynamicType               * dt     = NULL;

  if ( ( type_folder == NULL ) ||
       ( type_file == NULL ) ) {
    return NULL;
  }
  
  if ( dp )
    {
      DDS::DynamicTypeBuilderFactory * dtbf   =
        DDS::DynamicTypeBuilderFactoryXml::get_instance( );
      if ( dtbf )
        {
          std::string file_path = std::string(type_folder) + "/xml/" + std::string(type_file) + ".xml";
          
          DDS::DynamicTypeBuilder        * dtb  =
            dtbf->create_type_w_uri ( file_path.c_str(),
                                      type_name,
                                      NULL );
          if ( dtb )
            {
              dt = dtb->build( );
              dtbf->delete_type_builder( dtb );
            }
        }
    }
  return dt;
}

DDS::ReturnCode_t
register_type( DDS::DomainParticipant * dp,
               DDS::DynamicType       * dt,
               const char             * type_name )
{
  DDS::ReturnCode_t              retval = DDS::RETCODE_ERROR;
  if ( dp && dt && type_name )
    {
      DDS::DynamicTypeSupport * dts =
        DDS::DynamicTypeSupport::create_type_support ( dt );
      if ( dts )
        {
          retval = dts->register_type( dp, type_name );
        }
    }
  return retval;
}

void
cleanup_type( DDS::DomainParticipant * dp,
              DDS::DynamicType       * dt )
{
  if ( dp && dt )
    {
      DDS::DynamicTypeBuilderFactory * dtbf   =
        DDS::DynamicTypeBuilderFactoryXml::get_instance( );
      dtbf->delete_type( dt );
    }
}

DDS::DynamicData *
create_data( DDS::DynamicType       * dt )
{
  DDS::DynamicData * retval = NULL;
  DDS::DynamicDataFactory * ddf = DDS::DynamicDataFactory::get_instance();
  if ( ddf )
    {
      retval = ddf->create_data( dt );
    }
  return retval;
}

DDS::ReturnCode_t
init_data( DDS::DynamicData    * dd,
           const char *data_folder,
           const char *data_file)
{
  DDS::ReturnCode_t              retval = DDS::RETCODE_ERROR;
  if ( ( data_folder == NULL ) ||
       ( data_file == NULL ) )
    {
      // retval = DDS::RETCODE_OK;
    }
  else
    {
      if ( dd )
        {
          std::string file_path = std::string(data_folder) + "/xml/" + std::string(data_file) + ".xml";
          retval = coredx::DynamicData_init_from_xmluri( dd, file_path.c_str() );
        }
    }

  return retval;
}

void
print_typeid_v1(DDS::DynamicType *dt) {
  DDS::TypeObject * tobj_v1 = DDS::DynamicType_to_TypeObject( dt );
  if ( tobj_v1 )
    {
      // assume it is a constructed type (it should be)
      uint64_t type_id = tobj_v1->the_type.constructed_type_id();
      std::cout << "Type Object V1 - Type ID: " << type_id << std::endl;
    }
  delete tobj_v1;
}

void
print_typeid_v2(DDS::DynamicType *dt) {
  DDS_XTypes_TypeIdentifier tid;
  char buf[128];

  // minimal typeid:
  {
    DDS_XTypes_TypeIdentifier_init( &tid );
    CDX::DynamicTypeHelper::DynamicType_to_TypeIdentifier( dt, &tid, DDS_XTypes_EK_MINIMAL );
    memset(buf, 0, sizeof(buf));
    DDS_XTypes_TypeIdentifier_to_str( &tid, buf, 128 );
    char * buf_ptr = &buf[2]; // advance past the prefix we add to the typeid string ("C_" or "M_")
    std::cout << "Minimal Type Object V2 - Equivalence Hash: " << buf_ptr << std::endl;
    DDS_XTypes_TypeIdentifier_clear( &tid );
  }
  // complete typeid:
  {
    DDS_XTypes_TypeIdentifier_init( &tid );
    CDX::DynamicTypeHelper::DynamicType_to_TypeIdentifier( dt, &tid, DDS_XTypes_EK_COMPLETE );
    memset(buf, 0, sizeof(buf));
    DDS_XTypes_TypeIdentifier_to_str( &tid, buf, 128 );
    char * buf_ptr = &buf[2]; // advance past the prefix we add to the typeid string ("C_" or "M_")
    std::cout << "Complete Type Object V2 - Equivalence Hash: " << buf_ptr << std::endl;
    DDS_XTypes_TypeIdentifier_clear( &tid );
  }
  
}

void
print_typeid(DDS::DynamicType *dt, int version)
{
    if (version == 1) {
        print_typeid_v1(dt);
    } else if (version == 2) {
        print_typeid_v2(dt);
    } else {
        std::cerr << "Unsupported Type Object version: " << version
                << ". Cannot print type information." << std::endl;
    }
}
   
void
print_data( DDS::DynamicData  * dd )
{
  coredx::DynamicData_print_xml( stdout, dd, 0 );
}

void
cleanup_data( DDS::DynamicData *dd )
{
  DDS::DynamicDataFactory * ddf = DDS::DynamicDataFactory::get_instance();
  ddf->delete_data( dd );
}


bool
check_data( DDS::DynamicData *dd,
            const char *data_folder,
            const char *data_file )
{
  bool retval = false;
  
  if ( ( data_folder == NULL ) ||
       ( data_file == NULL ) )
    {
      retval = DDS::RETCODE_OK;
    }
  else
    {
      DDS::DynamicData *data_check =
        create_data( (DDS::DynamicType *) dd->get_type() );
      
      if ( data_check == NULL ) {
        retval = false;
        
      } else {

        if ( init_data( data_check, data_folder, data_file ) != DDS_RETCODE_OK ) {
          retval = false;
          
        } else {
          
          retval = dd->equals( data_check );
          
          if ( !retval )
            {
              printf("Expected:\n");
              print_data( data_check );
            }
          
        }
        
        if ( data_check != NULL ) {
          cleanup_data( data_check );
        }
      }
    }
  return retval;
}
