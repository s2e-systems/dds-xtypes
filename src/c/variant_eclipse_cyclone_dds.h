#include "dds/dds.h"

#define DDS_BOOLEAN_TRUE         (1)
#define DDS_BOOLEAN_FALSE        (0)
#define LISTENER_STATUS_MASK_ALL (ALL_STATUS)

const char* get_qos_policy_name(uint32_t last_policy_id) {

    switch (last_policy_id) {
        case DDS_INVALID_QOS_POLICY_ID: return "INVALID"; 
        case DDS_USERDATA_QOS_POLICY_ID: return "USERDATA"; 
        case DDS_DURABILITY_QOS_POLICY_ID: return "DURABILITY"; 
        case DDS_PRESENTATION_QOS_POLICY_ID: return "PRESENTATION"; 
        case DDS_DEADLINE_QOS_POLICY_ID: return "DEADLINE"; 
        case DDS_LATENCYBUDGET_QOS_POLICY_ID: return "LATENCYBUDGET"; 
        case DDS_OWNERSHIP_QOS_POLICY_ID: return "OWNERSHIP"; 
        case DDS_OWNERSHIPSTRENGTH_QOS_POLICY_ID: return "OWNERSHIPSTRENGTH"; 
        case DDS_LIVELINESS_QOS_POLICY_ID: return "LIVELINESS"; 
        case DDS_TIMEBASEDFILTER_QOS_POLICY_ID: return "TIMEBASEDFILTER"; 
        case DDS_PARTITION_QOS_POLICY_ID: return "PARTITION"; 
        case DDS_RELIABILITY_QOS_POLICY_ID: return "RELIABILITY"; 
        case DDS_DESTINATIONORDER_QOS_POLICY_ID: return "DESTINATIONORDER"; 
        case DDS_HISTORY_QOS_POLICY_ID: return "HISTORY"; 
        case DDS_RESOURCELIMITS_QOS_POLICY_ID: return "RESOURCELIMITS"; 
        case DDS_ENTITYFACTORY_QOS_POLICY_ID: return "ENTITYFACTORY"; 
        case DDS_WRITERDATALIFECYCLE_QOS_POLICY_ID: return "WRITERDATALIFECYCLE"; 
        case DDS_READERDATALIFECYCLE_QOS_POLICY_ID: return "READERDATALIFECYCLE"; 
        case DDS_TOPICDATA_QOS_POLICY_ID: return "TOPICDATA"; 
        case DDS_GROUPDATA_QOS_POLICY_ID: return "GROUPDATA"; 
        case DDS_TRANSPORTPRIORITY_QOS_POLICY_ID: return "TRANSPORTPRIORITY"; 
        case DDS_LIFESPAN_QOS_POLICY_ID: return "LIFESPAN"; 
        case DDS_DURABILITYSERVICE_QOS_POLICY_ID: return "DURABILITYSERVICE"; 
        case DDS_PROPERTY_QOS_POLICY_ID: return "PROPERTY"; 
        case DDS_TYPE_CONSISTENCY_ENFORCEMENT_QOS_POLICY_ID: return "TYPE_CONSISTENCY_ENFORCEMENT"; 
        case DDS_DATA_REPRESENTATION_QOS_POLICY_ID: return "DATAREPRESENTATION";
        default:
            return 0; 
    }
}

dds_dynamic_type_t  *
CREATE_TYPE( dds_entity_t dp,
             const char * types_uri,
             const char * type_name )
{
  dds_dynamic_type_t* dt     = NULL;
  if ( dp && types_uri && type_name )
    {
      DDS::DynamicTypeBuilderFactory * dtbf   =
        DDS::DynamicTypeBuilderFactoryXml::get_instance( );
      if ( dtbf )
        {
          DDS::DynamicTypeBuilder        * dtb  =
            dtbf->create_type_w_uri ( types_uri,
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

dds_return_t
REGISTER_TYPE( dds_entity_t        dp,
               dds_dynamic_type_t* dt,
               const char*         type_name )
{
  dds_return_t retval = DDS_RETCODE_ERROR;
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
CLEANUP_TYPE( dds_entity_t        dp,
              dds_dynamic_type_t* dt )
{
  if ( dp && dt )
    {
      DDS::DynamicTypeBuilderFactory * dtbf   =
        DDS::DynamicTypeBuilderFactoryXml::get_instance( );
      dtbf->delete_type( dt );
    }
}

DDS::DynamicData *
CREATE_DATA( DDS::DynamicType       * dt )
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
INIT_DATA( DDS::DynamicData    * dd,
           const char          * xml_data_uri,
           const char          * json_data_uri )
{
  DDS::ReturnCode_t              retval = DDS::RETCODE_ERROR;
  if ( dd )
    {
      fflush( stderr );
      if ( xml_data_uri )
        {
          retval = coredx::DynamicData_init_from_xmluri( dd, xml_data_uri );
        }
      else
        {
          /* no specific data, just init to 'defaults' */
          fprintf( stderr, "[ No data to load. Using empty sample... ]\n" );
          fflush( stderr );
          retval = DDS::RETCODE_OK;
        }
    }
  return retval;
}
   
void
PRINT_DATA( DDS::DynamicData  * dd )
{
  // coredx::DynamicData_print( stderr, dd, 0 );
  coredx::DynamicData_print_xml( stdout, dd, 0 );
}

void CLEANUP_DATA(DDS::DynamicData *dd)
{
  DDS::DynamicDataFactory * ddf = DDS::DynamicDataFactory::get_instance();
  ddf->delete_data( dd );
}


bool
CHECK_DATA(DDS::DynamicData *dd,
           const char *xml_data_uri,
           const char *json_data_uri)
{
  bool retval = false;

  if (dd == NULL && json_data_uri == NULL) {
    return retval;
  }

  DDS::DynamicData *data_check =
    CREATE_DATA( (DDS::DynamicType *) dd->get_type() );
  
  if (data_check == NULL) {
    retval = false;
    goto done;
  }
  if (INIT_DATA(data_check, xml_data_uri, json_data_uri) != DDS_RETCODE_OK) {
    retval = false;
    goto done;
  }

  retval = dd->equals(data_check);
  if ( !retval )
    {
      printf("Expected:\n");
      PRINT_DATA( data_check );
    }
  
 done:
  if (data_check != NULL) {
    CLEANUP_DATA(data_check);
  }
  return retval;
}
