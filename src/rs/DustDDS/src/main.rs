use clap::{Parser, ValueEnum};
use ctrlc;
use dust_dds::{
    dds_async::topic_description::TopicDescriptionAsync,
    domain::{
        domain_participant::DomainParticipant,
        domain_participant_factory::DomainParticipantFactory,
        domain_participant_listener::DomainParticipantListener,
    },
    infrastructure::{
        error::DdsError,
        listener::NO_LISTENER,
        qos::{DataReaderQos, DataWriterQos, PublisherQos, QosKind, SubscriberQos},
        qos_policy::{
            self, DataRepresentationQosPolicy, DurabilityQosPolicy, HistoryQosPolicy,
            HistoryQosPolicyKind, OwnershipQosPolicy, OwnershipQosPolicyKind,
            OwnershipStrengthQosPolicy, PartitionQosPolicy, ReliabilityQosPolicy,
            XCDR_DATA_REPRESENTATION, XCDR2_DATA_REPRESENTATION,
        },
        sample_info::{ANY_INSTANCE_STATE, ANY_SAMPLE_STATE, ANY_VIEW_STATE},
        status::{NO_STATUS, StatusKind},
        time::DurationKind,
    },
    publication::data_writer::DataWriter,
    subscription::data_reader::DataReader,
    xtypes::dynamic_type::{
        DynamicData, DynamicDataFactory, DynamicType, DynamicTypeBuilderFactory,
    },
};
use std::{
    fmt::Debug,
    process::{ExitCode, Termination},
    sync::mpsc::Receiver,
};

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
#[clap(rename_all = "kebab_case")]
enum TypeConsistencyArg {
    /// True
    T,
    /// False
    F,
    /// Default
    D,
}

#[derive(Parser, Clone)]
#[command(author, version, about, long_about = None)]
struct Options {
    /// domain id (default: 0)
    #[clap(short = 'd', default_value_t = 0)]
    domain_id: i32,

    /// BEST_EFFORT reliability
    #[clap(short = 'b', default_value_t = false)]
    best_effort_reliability: bool,

    /// RELIABLE reliability
    #[clap(short = 'r', default_value_t = false)]
    reliable_reliability: bool,

    /// keep history depth [0: KEEP_ALL]
    #[clap(short = 'k', default_value_t = -1, allow_negative_numbers = true)]
    history_depth: i32,

    /// set a 'deadline' with interval (seconds) [0: OFF]
    #[clap(short = 'f', default_value_t = 0)]
    deadline_interval: u64,

    /// apply 'time based filter' with interval (seconds) [0: OFF]
    #[clap(short = 'i', default_value_t = 0)]
    timebasedfilter_interval: u64,

    /// set ownership strength [-1: SHARED]
    #[clap(short = 's', default_value_t = -1, allow_negative_numbers = true)]
    ownership_strength: i32,

    /// set the topic name
    #[clap(short = 't')]
    topic_name: Option<String>,

    /// set the type name
    #[clap(short = 'y')]
    type_name: Option<String>,

    /// set a 'partition' string
    #[clap(short = 'p')]
    partition: Option<String>,

    /// set durability [v: VOLATILE,  l: TRANSIENT_LOCAL, t: TRANSIENT, p: PERSISTENT]
    #[clap(short = 'D', default_value_t = 'v')]
    durability_kind: char,

    /// publish samples
    #[clap(short = 'P', default_value_t = false)]
    publish: bool,

    /// subscribe samples
    #[clap(short = 'S', default_value_t = false)]
    subscribe: bool,

    /// set data representation [1: XCDR, 2: XCDR2]
    #[clap(short = 'x', default_value_t = 1)]
    data_representation: u16,

    /// folder containing type definitions (eg: types)
    #[clap(long)]
    type_folder: Option<String>,

    /// type definition file name without extension
    #[clap(long)]
    type_file: Option<String>,

    /// folder containing data samples (eg: data)
    #[clap(long)]
    data_folder: Option<String>,

    /// data sample file name without extension
    #[clap(long)]
    data_file: Option<String>,

    /// print Publisher's samples
    #[clap(short = 'w', default_value_t = false)]
    print_writer_samples: bool,

    /// enable, disable or default value for type_consistency.force_type_validation
    #[clap(long)]
    force_type_validation: Option<TypeConsistencyArg>,

    /// enable, disable or default value for type_consistency.ignore_member_names
    #[clap(long)]
    ignore_member_names: Option<TypeConsistencyArg>,

    /// enable, disable or default value for type_consistency.ignore_sequence_bounds
    #[clap(long)]
    ignore_seq_bounds: Option<TypeConsistencyArg>,

    /// enable, disable or default value for type_consistency.ignore_string_bounds
    #[clap(long)]
    ignore_str_bounds: Option<TypeConsistencyArg>,

    /// enable, disable or default value for type_consistency.prevent_type_widening
    #[clap(long)]
    prevent_type_widening: Option<TypeConsistencyArg>,

    /// enable, disable type coercion or default value for type_consistency.kind
    #[clap(long)]
    allow_type_coercion: Option<TypeConsistencyArg>,

    /// disable sending the type info for type assignability
    #[clap(long, default_value_t = false)]
    disable_type_info: bool,

    /// set the Type Object version to use. Default: 2.
    #[clap(long, default_value_t = 2)]
    type_object_version: u32,

    /// print typeid (TypeObjectV1) or equivalence hash (TypeObjectV2)
    #[clap(long, default_value_t = false)]
    print_typeid: bool,

    /// set log message verbosity [e: ERROR, d: DEBUG]
    #[clap(short = 'v', default_value_t = 'e')]
    log_message_verbosity: char,
}

impl Options {
    fn validate(&self) -> Result<(), ParsingError> {
        if self.topic_name.is_none() {
            return Err(ParsingError(
                "topic name unspecified [-t], using \"test\" by default".to_string(),
            ));
        }
        if self.type_name.is_none() {
            return Err(ParsingError("please specify type name [-y]".to_string()));
        }
        if !self.publish && !self.subscribe {
            return Err(ParsingError(
                "please specify publish [-P] or subscribe [-S]".to_string(),
            ));
        }
        if self.publish && self.subscribe {
            return Err(ParsingError(
                "please specify only one of: publish [-P] or subscribe [-S]".to_string(),
            ));
        }
        if self.type_folder.is_none() && self.type_file.is_none() {
            return Err(ParsingError(
                "please provide the types via --type-folder or --type-file".to_string(),
            ));
        }
        Ok(())
    }

    fn reliability_qos_policy(&self) -> ReliabilityQosPolicy {
        let mut reliability = DataWriterQos::default().reliability;
        if self.best_effort_reliability {
            reliability.kind = qos_policy::ReliabilityQosPolicyKind::BestEffort;
        }
        if self.reliable_reliability {
            reliability.kind = qos_policy::ReliabilityQosPolicyKind::Reliable;
        }
        reliability
    }

    fn partition_qos_policy(&self) -> PartitionQosPolicy {
        if let Some(partition) = &self.partition {
            PartitionQosPolicy {
                name: vec![partition.to_owned()],
            }
        } else {
            PartitionQosPolicy::default()
        }
    }

    fn durability_qos_policy(&self) -> DurabilityQosPolicy {
        DurabilityQosPolicy {
            kind: match self.durability_kind {
                'v' => qos_policy::DurabilityQosPolicyKind::Volatile,
                'l' => qos_policy::DurabilityQosPolicyKind::TransientLocal,
                't' => qos_policy::DurabilityQosPolicyKind::Transient,
                'p' => qos_policy::DurabilityQosPolicyKind::Persistent,
                _ => panic!("durability not valid"),
            },
        }
    }

    fn data_representation_qos_policy(&self) -> DataRepresentationQosPolicy {
        let data_representation = match self.data_representation {
            1 => XCDR_DATA_REPRESENTATION,
            2 => XCDR2_DATA_REPRESENTATION,
            _ => panic!("Wrong data representation"),
        };
        qos_policy::DataRepresentationQosPolicy {
            value: vec![data_representation],
        }
    }

    fn ownership_qos_policy(&self) -> OwnershipQosPolicy {
        OwnershipQosPolicy {
            kind: match self.ownership_strength {
                -1 => qos_policy::OwnershipQosPolicyKind::Shared,
                _ => qos_policy::OwnershipQosPolicyKind::Exclusive,
            },
        }
    }

    fn history_depth_qos_policy(&self) -> HistoryQosPolicy {
        match self.history_depth {
            -1 => HistoryQosPolicy::default(),
            0 => HistoryQosPolicy {
                kind: HistoryQosPolicyKind::KeepAll,
            },
            x if x >= 1 => HistoryQosPolicy {
                kind: HistoryQosPolicyKind::KeepLast(x as u32),
            },
            _ => panic!("history_depth not valid"),
        }
    }

    fn ownership_strength_qos_policy(&self) -> OwnershipStrengthQosPolicy {
        if self.ownership_strength < -1 {
            panic!("Ownership strength must be positive or zero")
        }
        OwnershipStrengthQosPolicy {
            value: self.ownership_strength,
        }
    }
}

struct Listener;
impl DomainParticipantListener for Listener {
    fn on_publication_matched(
        &mut self,
        the_writer: dust_dds::dds_async::data_writer::DataWriterAsync<()>,
        status: dust_dds::infrastructure::status::PublicationMatchedStatus,
    ) -> impl Future<Output = ()> + Send {
        let topic_name = the_writer.get_topic().get_name();
        let type_name = the_writer.get_topic().get_type_name();
        println!(
            "on_publication_matched() topic: '{}'  type: '{}' : matched readers {} (change = {})",
            topic_name, type_name, status.current_count, status.current_count_change
        );
        core::future::ready(())
    }

    fn on_subscription_matched(
        &mut self,
        the_reader: dust_dds::dds_async::data_reader::DataReaderAsync<()>,
        status: dust_dds::infrastructure::status::SubscriptionMatchedStatus,
    ) -> impl Future<Output = ()> + Send {
        let topic_name = the_reader.get_topicdescription().get_name();
        let type_name = the_reader.get_topicdescription().get_type_name();
        println!(
            "on_subscription_matched() topic: '{}'  type: '{}' : matched writers {} (change = {})",
            topic_name, type_name, status.current_count, status.current_count_change
        );
        core::future::ready(())
    }

    fn on_liveliness_changed(
        &mut self,
        the_reader: dust_dds::dds_async::data_reader::DataReaderAsync<()>,
        status: dust_dds::infrastructure::status::LivelinessChangedStatus,
    ) -> impl Future<Output = ()> + Send {
        let topic_name = the_reader.get_topicdescription().get_name();
        let type_name = the_reader.get_topicdescription().get_type_name();
        println!(
            "on_liveliness_changed() topic: '{}'  type: '{}' : (alive = {}, not_alive = {}",
            topic_name, type_name, status.alive_count, status.not_alive_count
        );
        core::future::ready(())
    }
}

fn init_publisher(
    participant: &DomainParticipant,
    options: Options,
    dynamic_type: DynamicType<'static>,
) -> Result<DataWriter<DynamicData<'static>>, InitializeError> {
    let topic_name = options.topic_name.clone().unwrap_or("test".to_string());
    let type_name = options.type_name.clone().unwrap();

    let topic = participant.create_dynamic_topic(
        &topic_name,
        &type_name,
        QosKind::Default,
        NO_LISTENER,
        NO_STATUS,
        dynamic_type,
    )?;

    println!("Create topic: {}", topic_name);

    let publisher_qos = QosKind::Specific(PublisherQos {
        partition: options.partition_qos_policy(),
        ..Default::default()
    });
    let publisher = participant.create_publisher(publisher_qos, NO_LISTENER, NO_STATUS)?;

    let mut data_writer_qos = DataWriterQos {
        durability: options.durability_qos_policy(),
        reliability: options.reliability_qos_policy(),
        representation: options.data_representation_qos_policy(),
        ownership: options.ownership_qos_policy(),
        history: options.history_depth_qos_policy(),
        ..Default::default()
    };
    if options.deadline_interval > 0 {
        data_writer_qos.deadline.period =
            DurationKind::Finite(core::time::Duration::from_secs(options.deadline_interval).into());
    }
    if options.ownership_qos_policy().kind == OwnershipQosPolicyKind::Exclusive {
        data_writer_qos.ownership_strength = options.ownership_strength_qos_policy();
    }

    println!(
        "Create writer for topic: {} type: {}",
        topic_name, type_name
    );

    let data_writer = publisher.create_datawriter::<DynamicData>(
        &topic,
        QosKind::Specific(data_writer_qos),
        NO_LISTENER,
        NO_STATUS,
    )?;

    Ok(data_writer)
}

fn run_publisher(
    data_writer: &DataWriter<DynamicData<'static>>,
    options: Options,
    dynamic_type: DynamicType<'static>,
    all_done: Receiver<()>,
) -> Result<(), RunningError> {
    let mut dd = DynamicDataFactory::create_data(dynamic_type);

    // Attempt to load JSON data into DynamicData
    if let (Some(data_folder), Some(data_file)) = (&options.data_folder, &options.data_file) {
        let file_path = format!("{}/xml/{}.xml", data_folder, data_file);
        if let Ok(content) = std::fs::read_to_string(&file_path) {
            dd.from_xml(&content)
                .map_err(|e| RunningError(format!("{e:?}")))?;
        }
    }

    while all_done.try_recv().is_err() {
        if options.print_writer_samples {
            println!(" Wrote:");
        }
        // Write dynamic data
        data_writer.write(dd.clone(), None).ok();
        std::thread::sleep(std::time::Duration::from_secs(1));
    }
    Ok(())
}

fn init_subscriber(
    participant: &DomainParticipant,
    options: Options,
    dynamic_type: DynamicType<'static>,
) -> Result<DataReader<DynamicData<'static>>, InitializeError> {
    let topic_name = options.topic_name.clone().unwrap_or("test".to_string());
    let type_name = options.type_name.clone().unwrap();

    let topic = participant
        .create_dynamic_topic(
            &topic_name,
            &type_name,
            QosKind::Default,
            NO_LISTENER,
            NO_STATUS,
            dynamic_type,
        )
        .unwrap();

    println!("Create topic: {}", topic_name);

    let subscriber_qos = QosKind::Specific(SubscriberQos {
        partition: options.partition_qos_policy(),
        ..Default::default()
    });
    let subscriber = participant.create_subscriber(subscriber_qos, NO_LISTENER, NO_STATUS)?;

    let mut data_reader_qos = DataReaderQos {
        durability: options.durability_qos_policy(),
        reliability: options.reliability_qos_policy(),
        representation: options.data_representation_qos_policy(),
        ownership: options.ownership_qos_policy(),
        history: options.history_depth_qos_policy(),
        ..Default::default()
    };
    if options.deadline_interval > 0 {
        data_reader_qos.deadline.period =
            DurationKind::Finite(core::time::Duration::from_secs(options.deadline_interval).into());
    }
    if options.timebasedfilter_interval > 0 {
        data_reader_qos.time_based_filter.minimum_separation = DurationKind::Finite(
            core::time::Duration::from_secs(options.timebasedfilter_interval).into(),
        );
    }

    // // Set type consistency enforcement based on arguments
    // let mut type_consistency = TypeConsistencyEnforcementQosPolicy::default();

    // if let Some(allow_type_coercion) = options.allow_type_coercion {
    //     match allow_type_coercion {
    //         TypeConsistencyArg::T => type_consistency.kind = TypeConsistencyKind::AllowTypeCoercion,
    //         TypeConsistencyArg::F => {
    //             type_consistency.kind = TypeConsistencyKind::DisallowTypeCoercion
    //         }
    //         TypeConsistencyArg::D => {
    //             type_consistency.kind = TypeConsistencyEnforcementQosPolicy::default().kind
    //         }
    //     }
    // }
    // if let Some(force_type_validation) = options.force_type_validation {
    //     match force_type_validation {
    //         TypeConsistencyArg::T => type_consistency.force_type_validation = true,
    //         TypeConsistencyArg::F => type_consistency.force_type_validation = false,
    //         TypeConsistencyArg::D => {
    //             type_consistency.force_type_validation =
    //                 TypeConsistencyEnforcementQosPolicy::default().force_type_validation
    //         }
    //     }
    // }
    // if let Some(ignore_member_names) = options.ignore_member_names {
    //     match ignore_member_names {
    //         TypeConsistencyArg::T => type_consistency.ignore_member_names = true,
    //         TypeConsistencyArg::F => type_consistency.ignore_member_names = false,
    //         TypeConsistencyArg::D => {
    //             type_consistency.ignore_member_names =
    //                 TypeConsistencyEnforcementQosPolicy::default().ignore_member_names
    //         }
    //     }
    // }
    // if let Some(ignore_seq_bounds) = options.ignore_seq_bounds {
    //     match ignore_seq_bounds {
    //         TypeConsistencyArg::T => type_consistency.ignore_sequence_bounds = true,
    //         TypeConsistencyArg::F => type_consistency.ignore_sequence_bounds = false,
    //         TypeConsistencyArg::D => {
    //             type_consistency.ignore_sequence_bounds =
    //                 TypeConsistencyEnforcementQosPolicy::default().ignore_sequence_bounds
    //         }
    //     }
    // }
    // if let Some(ignore_str_bounds) = options.ignore_str_bounds {
    //     match ignore_str_bounds {
    //         TypeConsistencyArg::T => type_consistency.ignore_string_bounds = true,
    //         TypeConsistencyArg::F => type_consistency.ignore_string_bounds = false,
    //         TypeConsistencyArg::D => {
    //             type_consistency.ignore_string_bounds =
    //                 TypeConsistencyEnforcementQosPolicy::default().ignore_string_bounds
    //         }
    //     }
    // }
    // if let Some(prevent_type_widening) = options.prevent_type_widening {
    //     match prevent_type_widening {
    //         TypeConsistencyArg::T => type_consistency.prevent_type_widening = true,
    //         TypeConsistencyArg::F => type_consistency.prevent_type_widening = false,
    //         TypeConsistencyArg::D => {
    //             type_consistency.prevent_type_widening =
    //                 TypeConsistencyEnforcementQosPolicy::default().prevent_type_widening
    //         }
    //     }
    // }

    // data_reader_qos.type_consistency = type_consistency;

    println!("Create reader for topic: {}", topic_name);

    let data_reader = subscriber.create_datareader::<DynamicData>(
        &topic,
        QosKind::Specific(data_reader_qos),
        NO_LISTENER,
        NO_STATUS,
    )?;

    Ok(data_reader)
}


// static void print_sample1_to (struct type_cache *tc, const unsigned char *sample, const DDS_XTypes_CompleteTypeObject *typeobj, struct context *c, const char *label, bool is_base_type, bool is_opt)
// {
//   if (print_sample1_simple (sample, typeobj->_d, c, label, NULL, is_opt))
//     return;
//   switch (typeobj->_d)
//   {
//     case DDS_XTypes_TK_ALIAS: {
//       print_sample1_ti (tc, sample, &typeobj->_u.alias_type.body.common.related_type, 0, c, label, false, is_opt);
//       break;
//     }
//     case DDS_XTypes_TK_SEQUENCE: {
//       const DDS_XTypes_TypeIdentifier *et = &typeobj->_u.sequence_type.element.common.type;
//       const dds_sequence_t *p = align (sample, c, _Alignof (dds_sequence_t), sizeof (dds_sequence_t));
//       struct context c1 = { .key = c->key, .valid_data = c->valid_data, .offset = 0, .maxalign = 1, .needs_comma = false };
//       if (c->needs_comma) fputc (',', stdout);
//       if (label) printf ("\"%s\":", label);
//       printf ("[");
//       for (uint32_t i = 0; i < p->_length; i++)
//       {
//         print_sample1_ti (tc, (const unsigned char *) p->_buffer, et, 0, &c1, NULL, false, false);
//         finish_sequence_element (&c1);
//       }
//       printf ("]");
//       c->needs_comma = true;
//       break;
//     }
//     case DDS_XTypes_TK_STRUCTURE: {
//       struct typeinfo *info = type_cache_lookup_typeobj (tc, typeobj);
//       const DDS_XTypes_CompleteStructType *t = &typeobj->_u.struct_type;
//       const unsigned char *p = align (sample, c, info->align, info->size);
//       if (c->needs_comma) fputc (',', stdout);
//       if (label) printf ("\"%s\":", label);
//       if (!is_base_type) { printf ("{"); c->needs_comma = false; }
//       struct context c1 = { .key = c->key, .valid_data = c->valid_data, .offset = 0, .maxalign = 1, .needs_comma = c->needs_comma };
//       if (t->header.base_type._d != DDS_XTypes_TK_NONE)
//         print_sample1_ti (tc, p, &t->header.base_type, 0, &c1, NULL, true, false);
//       for (uint32_t i = 0; i < t->member_seq._length; i++)
//       {
//         const DDS_XTypes_CompleteStructMember *m = &t->member_seq._buffer[i];
//         c1.key = c->key && (m->common.member_flags & DDS_XTypes_IS_KEY);
//         if (!is_indirect_member (m->common.member_flags)) {
//           print_sample1_ti (tc, p, &m->common.member_type_id, 0, &c1, *m->detail.name ? m->detail.name : NULL, false, false);
//         } else {
//           void const * const *p1 = (const void *) align (p, &c1, _Alignof (void *), sizeof (void *));
//           if (c1.key || c->valid_data) {
//             if (*p1 != NULL) { // missing optional/external values are not visible at all in the output
//               struct context c2 = { .key = c1.key && !is_optional_member (m->common.member_flags), .valid_data = c1.valid_data, .offset = 0, .maxalign = 1, .needs_comma = c1.needs_comma };
//               print_sample1_ti (tc, *p1, &m->common.member_type_id, 0, &c2, *m->detail.name ? m->detail.name : NULL, false, true);
//               c1.needs_comma = c2.needs_comma;
//             }
//           }
//         }
//       }
//       if (!is_base_type) {
//         printf ("}");
//         c1.needs_comma = true;
//       }
//       c->needs_comma = c1.needs_comma;
//       break;
//     }
//     case DDS_XTypes_TK_ENUM: {
//       struct typeinfo *info = type_cache_lookup_typeobj (tc, typeobj);
//       const DDS_XTypes_CompleteEnumeratedType *t = &typeobj->_u.enumerated_type;
//       const int *p = align (sample, c, info->align, info->size);
//       if (c->key || c->valid_data)
//       {
//         if (c->needs_comma) fputc (',', stdout);
//         if (label) printf ("\"%s\":", label);
//         for (uint32_t l = 0; l < t->literal_seq._length; l++)
//         {
//           if (t->literal_seq._buffer[l].common.value == *p)
//             printf ("\"%s\"", t->literal_seq._buffer[l].detail.name);
//         }
//         c->needs_comma = true;
//       }
//       break;
//     }
//     case DDS_XTypes_TK_BITMASK: {
//       struct typeinfo *info = type_cache_lookup_typeobj (tc, typeobj);
//       const DDS_XTypes_CompleteBitmaskType *t = &typeobj->_u.bitmask_type;
//       const void *p = align (sample, c, info->align, info->size);
//       if (c->key || c->valid_data)
//       {
//         if (c->needs_comma) fputc (',', stdout);
//         if (label) printf ("\"%s\":", label);
//         printf ("%"PRIu64, read_bitmask_value (p, t->header.common.bit_bound));
//         c->needs_comma = true;
//       }
//       break;
//     }
//     case DDS_XTypes_TK_UNION: {
//       struct typeinfo *info = type_cache_lookup_typeobj (tc, typeobj);
//       const DDS_XTypes_CompleteUnionType *t = &typeobj->_u.union_type;
//       const unsigned char *p = align (sample, c, info->align, info->size);
//       if (c->needs_comma) fputc (',', stdout);
//       if (label) printf ("\"%s\":", label);
//       printf ("{");
//       int32_t disc_value = 0;
//       struct context c1 = { .key = c->key, .valid_data = c->valid_data, .offset = 0, .maxalign = 1, .needs_comma = false };
//       if (t->discriminator.common.type_id._d == DDS_XTypes_EK_COMPLETE)
//       {
//         struct typeinfo *info_disc = type_cache_lookup_typeid (tc, &t->discriminator.common.type_id);
//         if (info_disc->typeobj->_d == DDS_XTypes_TK_ENUM)
//         {
//           disc_value = * (int32_t *) p;
//         }
//         else if (info_disc->typeobj->_d == DDS_XTypes_TK_BITMASK)
//         {
//           if (info_disc->typeobj->_u.bitmask_type.header.common.bit_bound > 32)
//             disc_value = (int32_t) (* (int64_t *) p);
//           else if (info_disc->typeobj->_u.bitmask_type.header.common.bit_bound > 16)
//             disc_value = * (int32_t *) p;
//           else if (info_disc->typeobj->_u.bitmask_type.header.common.bit_bound > 8)
//             disc_value = * (int16_t *) p;
//           else
//             disc_value = * (int8_t *) p;
//         }
//         else
//         {
//           printf ("unsupported union discriminant value %u\n", info_disc->typeobj->_d);
//           abort ();
//         }
//         print_sample1_to (tc, p, info_disc->typeobj, &c1, "_d", false, false);
//       }
//       else if (!print_sample1_simple (p, t->discriminator.common.type_id._d, &c1, "_d", &disc_value, false))
//       {
//         abort ();
//       }
//       const DDS_XTypes_CompleteUnionMember *m = find_union_member_for_disc (t, disc_value);
//       if (m != NULL)
//       {
//         const unsigned char *data = p + type_cache_union_data_offset (tc, t);
//         struct context c2 = { .key = c1.key, .valid_data = c1.valid_data, .offset = 0, .maxalign = 1, .needs_comma = c1.needs_comma };
//         if (!is_indirect_member (m->common.member_flags))
//         {
//           print_sample1_ti (tc, data, &m->common.type_id, 0, &c2, *m->detail.name ? m->detail.name : NULL, false, false);
//         }
//         else
//         {
//           void const * const *p1 = (const void *) align (data, &c2, _Alignof (void *), sizeof (void *));
//           if ((c2.key || c2.valid_data) && *p1 != NULL)
//           {
//             struct context c3 = { .key = c2.key && !is_optional_member (m->common.member_flags), .valid_data = c2.valid_data, .offset = 0, .maxalign = 1, .needs_comma = c2.needs_comma };
//             print_sample1_ti (tc, *p1, &m->common.type_id, 0, &c3, *m->detail.name ? m->detail.name : NULL, false, true);
//             c2.needs_comma = c3.needs_comma;
//           }
//         }
//         c1.needs_comma = c2.needs_comma;
//       }
//       printf ("}");
//       c->needs_comma = true;
//     }
//   }
// }

// void dtl_print_sample (struct dyntypelib *dtl, bool valid_data, const void *sample, const DDS_XTypes_CompleteTypeObject *typeobj)
// {
//   struct context c1 = { .valid_data = valid_data, .key = true, .offset = 0, .maxalign = 1, .needs_comma = false };
//   print_sample1_to (dtl->typecache, sample, typeobj, &c1, NULL, false, false);
//   printf ("\n");
// }

fn run_subscriber(
    data_reader: &DataReader<DynamicData<'static>>,
    options: Options,
    dynamic_type: DynamicType<'static>,
    all_done: Receiver<()>,
) -> Result<(), RunningError> {
    let mut expected_data = None;
    if let (Some(data_folder), Some(data_file)) = (&options.data_folder, &options.data_file) {
        let file_path = format!("{}/xml/{}.xml", data_folder, data_file);
        if let Ok(content) = std::fs::read_to_string(&file_path) {
            let mut dd = DynamicDataFactory::create_data(dynamic_type);
            if dd.from_xml(&content).is_ok() {
                expected_data = Some(dd);
            }
        }
    }

    while all_done.try_recv().is_err() {
        let mut previous_handle = None;
        loop {
            let max_samples = i32::MAX;
            let read_result = data_reader.take_next_instance(
                max_samples,
                previous_handle,
                ANY_SAMPLE_STATE,
                ANY_VIEW_STATE,
                ANY_INSTANCE_STATE,
            );
            match read_result {
                Ok(samples) => {
                    for sample in samples {
                        if sample.sample_info.valid_data {
                            println!("sample_received()");
                            println!("sample.data {:?}", sample.data.as_ref().unwrap());
                            println!("expected_data {:?}", expected_data.as_ref().unwrap());
                            if let Some(expected) = &expected_data {
                                if sample.data.as_ref() == Some(expected) {
                                    println!("Received sample is the same as loaded");
                                } else {
                                    println!("Received sample is not the same as loaded");
                                }
                            }
                        }
                        previous_handle = Some(sample.sample_info.instance_handle);
                    }
                    std::thread::sleep(std::time::Duration::from_millis(100));
                }
                Err(_) => break,
            }
        }
    }
    Ok(())
}

fn initialize(options: &Options) -> Result<DomainParticipant, InitializeError> {
    let participant_factory = DomainParticipantFactory::get_instance();

    // Set domain participant factory QoS if needed

    let participant = participant_factory.create_participant(
        options.domain_id,
        QosKind::Default,
        Some(Listener),
        &[
            StatusKind::InconsistentTopic,
            StatusKind::OfferedIncompatibleQos,
            StatusKind::PublicationMatched,
            StatusKind::OfferedDeadlineMissed,
            StatusKind::LivelinessLost,
            StatusKind::RequestedIncompatibleQos,
            StatusKind::SubscriptionMatched,
            StatusKind::RequestedDeadlineMissed,
            StatusKind::LivelinessChanged,
        ],
    )?;

    Ok(participant)
}

struct ParsingError(String);
struct InitializeError(String);
struct RunningError(String);

impl From<DdsError> for InitializeError {
    fn from(value: DdsError) -> Self {
        Self(format!("DdsError: {:?}", value))
    }
}
impl From<DdsError> for RunningError {
    fn from(value: DdsError) -> Self {
        Self(format!("DdsError: {:?}", value))
    }
}

struct Return {
    code: u8,
    description: String,
}
impl Debug for Return {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_fmt(format_args!("code {}: {}", self.code, self.description))
    }
}

impl Termination for Return {
    fn report(self) -> ExitCode {
        self.code.into()
    }
}

impl From<ParsingError> for Return {
    fn from(value: ParsingError) -> Self {
        Self {
            code: 1,
            description: value.0,
        }
    }
}

fn main() -> Result<(), Return> {
    let (tx, rx) = std::sync::mpsc::channel();
    ctrlc::set_handler(move || {
        tx.send(()).expect("Could not send signal on channel.");
    })
    .expect("Error setting Ctrl-C handler");

    let mut options = Options::parse();
    if options.topic_name.is_none() {
        options.topic_name = Some("test".to_string());
    }

    if let Err(e) = options.validate() {
        return Err(e.into());
    }

    let participant = initialize(&options).map_err(|e| Return {
        code: 2,
        description: e.0,
    })?;

    // Create the type
    let mut dt = None;
    if let (Some(type_folder), Some(type_file), Some(type_name)) =
        (&options.type_folder, &options.type_file, &options.type_name)
    {
        let file_path = format!("{}/xml/{}.xml", type_folder, type_file);
        let type_xml = std::fs::read_to_string(file_path).unwrap();
        let type_builder =
            DynamicTypeBuilderFactory::create_type_w_document(&type_xml, type_name, vec![])
                .unwrap();
        dt = Some(type_builder.build());
    }

    if dt.is_none() {
        return Err(Return {
            code: 2,
            description: "Failed to create type".to_string(),
        });
    }

    // Since dt is checked above, it is Some
    let dt = dt.unwrap();

    if options.publish {
        let data_writer =
            init_publisher(&participant, options.clone(), dt).map_err(|e| Return {
                code: 2,
                description: e.0,
            })?;
        run_publisher(&data_writer, options.clone(), dt, rx).map_err(|e| Return {
            code: 3,
            description: e.0,
        })?;
    } else {
        let data_reader =
            init_subscriber(&participant, options.clone(), dt).map_err(|e| Return {
                code: 2,
                description: e.0,
            })?;
        run_subscriber(&data_reader, options.clone(), dt, rx).map_err(|e| Return {
            code: 3,
            description: e.0,
        })?;
    }

    println!("Done.");

    Ok(())
}
