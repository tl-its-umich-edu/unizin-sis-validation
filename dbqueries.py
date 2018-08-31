# SisIntId,SisExtId,FirstName,MiddleName,LastName,Suffix,Sex,Ethnicity,ZipCode,USResidency,HsGpa,ColGpaCum,ActiveDuty,Veteran,EduLevelPaternal,EduLevelMaternal,EduLevelParental,EnrollmentLevel,CourseCount,SatMathPre2016,SatMathPost2016,SatMathCombined,SatVerbalPre2016,SatReadingPost2016,SatVerbalReadingCombined,SatWritingPre2016,SatWritingPost2016,SatWritingCombined,SatTotalCombined,ActReading,ActMath,ActEnglish,ActScience,ActComposite,PhoneNumber,PhoneType,EmailAddress,EmailType
# CSV Has Prefix Data has Suffix
# Currently missing HsGpa ColGpaCum EduLevelPaternal EduLevel Maternal EnrollmentLevelCourseCount Sat*
# Query for person rescord

QUERIES = { 
  'person' : {
    'index' : 'sisintid',
    'sis_file' : '{date}%2FPerson_{date}.csv',
    'query' : """
            SELECT
              ucdmint.sourcekey as SisIntId,
              ucdmext.sourcekey as SisExtId,
              Person.Firstname as FirstName,
              Person.Middlename as MiddleName,
              Person.Lastname as LastName,
              Person.Prefix as Prefix,
              Person.GenerationCode as Suffix,
              RefSex.description as Sex,
              RefRace.Code as Ethnicity,
              PersonAddress.PostalCode as ZipCode,
              RefUSCitizenshipStatus.Code as UsResidency,
              RefMilitaryActiveStudentIndicator.Code as ActiveDuty,
              RefMilitaryVeteranStudentIndicator.Code as Veteran,
              PersonTelephone.TelephoneNumber as PhoneNumber,
              RefPersonTelephoneNumberType.Code as PhoneType,
              PersonEmailAddress.EmailAddress as EmailAddress,
              RefEmailType.Code as EmailType
            FROM Person
              LEFT JOIN RefSex on RefSex.RefSexId=Person.RefSexId
              LEFT JOIN PersonDemographicRace on PersonDemographicRace.PersonId=Person.PersonId
              LEFT JOIN RefRace on RefRace.RefRaceId=PersonDemographicRace.RefRaceId
              LEFT JOIN PersonAddress on PersonAddress.PersonId=Person.PersonId
              LEFT JOIN RefUSCitizenshipStatus on RefUSCitizenshipStatus.RefUSCitizenshipStatusId=Person.RefUSCitizenshipStatusId
              LEFT JOIN PersonMilitary on PersonMilitary.PersonId=Person.PersonId
              LEFT JOIN RefMilitaryActiveStudentIndicator on RefMilitaryActiveStudentIndicator.RefMilitaryActiveStudentIndicatorId=PersonMilitary.RefMilitaryActiveStudentIndicatorId
              LEFT JOIN RefMilitaryVeteranStudentIndicator on RefMilitaryVeteranStudentIndicator.RefMilitaryVeteranStudentIndicatorId=PersonMilitary.RefMilitaryVeteranStudentIndicatorId
              LEFT JOIN PersonEmailAddress on PersonEmailAddress.PersonId=Person.PersonId
              LEFT JOIN RefEmailType on RefEmailType.RefEmailTypeId=PersonEmailAddress.RefEmailTypeId
              LEFT JOIN PersonTelephone on PersonTelephone.PersonId=Person.PersonId
              LEFT JOIN RefPersonTelephoneNumberType on RefPersonTelephoneNumberType.RefPersonTelephoneNumberTypeId=PersonTelephone.RefPersonTelephoneNumberTypeId
              LEFT JOIN ucdmentitykeymap ucdmint on ucdmint.ucdmkey = Person.PersonId and ucdmint.ucdmentityid = 1 and ucdmint.systemprovisioningid = 1000
              LEFT JOIN ucdmentitykeymap ucdmext on ucdmext.ucdmkey = Person.PersonId and ucdmext.ucdmentityid = 1 and ucdmext.systemprovisioningid = 1001
  """},
  #SisIntId,SisExtId,TermId,CourseSubj,CourseNo,Title,Description,Status,AvailableCredits
  'course_offering' : {
    'index' : 'sisintid',
    'sis_file' : '{date}%2FCourse_Offering_{date}.csv',
    'query' : """
            SELECT
              'TODO' as SisIntId,
              'TODO' as SisExtId,
              PsCourse.OrganizationCalendarSessionId as TermId,
              Course.SubjectAbbreviation as CourseSubj,
              PsCourse.CourseNumber as CourseNo,
              PsCourse.CourseTitle as Title,
              Course.Description as Description,
              RefWorkflowState.Code as Status,
              Course.CreditValue as AvailableCredits,
              OrganizationCalendarSession.SessionName,
              RefSessionType.Code as SessionType
            FROM Course
              LEFT JOIN PsCourse on PsCourse.OrganizationId=Course.OrganizationId
              LEFT JOIN OrganizationCalendarSession on OrganizationCalendarSession.OrganizationCalendarSessionId=PsCourse.OrganizationCalendarSessionId
              LEFT JOIN RefCourseCreditUnit on RefCourseCreditUnit.RefCourseCreditUnitId=Course.RefCourseCreditUnitId
              LEFT JOIN RefWorkflowState on RefWorkflowState.RefWorkflowStateId=Course.RefWorkflowStateId
              LEFT JOIN RefSessionType on RefSessionType.RefSessionTypeId=OrganizationCalendarSession.RefSessionTypeId
  """},
  #SisIntId,SisExtId,CourseId,TermId,SectionNumber,DeliveryMode,MaxEnrollment
  'course_section' : {
    'index' : 'sisintid',
    'sis_file' : '{date}%2FCourse_Section_{date}.csv',
    'query' : """
            SELECT
              ucdmint.sourcekey as SisIntId,
              ucdmext.sourcekey as SisExtId,
              CourseSection.CourseId as CourseId,
              CourseSection.OrganizationCalendarSessionId as TermId,
              PsSection.SectionNumber as SectionNumber,
              RefCourseSectionDeliveryMode.Code as DeliveryMode,
              CourseSection.MaximumCapacity as MaxEnrollment,
              Organization.Name as Name,
              OrganizationCalendarSession.BeginDate as BeginDate,
              OrganizationCalendarSession.EndDate as EndDate,
              RefWorkflowState.Description as WorkflowState
            FROM CourseSection
              LEFT JOIN Organization on Organization.OrganizationId=CourseSection.OrganizationId
              LEFT JOIN PsSection on PsSection.OrganizationId=CourseSection.OrganizationId
              LEFT JOIN RefCourseSectionDeliveryMode on RefCourseSectionDeliveryMode.RefCourseSectionDeliveryModeId=CourseSection.RefCourseSectionDeliveryModeId
              LEFT JOIN RefCreditTypeEarned on RefCreditTypeEarned.RefCreditTypeEarnedId=CourseSection.RefCreditTypeEarnedId
              LEFT JOIN RefWorkflowState on RefWorkflowState.RefWorkflowStateId=CourseSection.RefWorkflowStateId
              LEFT JOIN OrganizationCalendarSession on OrganizationCalendarSession.OrganizationCalendarSessionId=CourseSection.OrganizationCalendarSessionId
              LEFT JOIN ucdmentitykeymap ucdmint on ucdmint.ucdmkey = CourseSection.OrganizationId and ucdmint.ucdmentityid = 5 and ucdmint.systemprovisioningid = 1000
              LEFT JOIN ucdmentitykeymap ucdmext on ucdmext.ucdmkey = CourseSection.OrganizationId and ucdmext.ucdmentityid = 5 and ucdmext.systemprovisioningid = 1001

  """},
  #SisIntId,SisExtId,TermType,SessionType,SessionName,TermBeginDate,TermEndDate,InstrBeginDate,InstrEndDate
  'calendar' : {
    'index' : 'sisintid',
    'sis_file' : '{date}%2FAcademic_Term_{date}.csv',
    'query' : """
            SELECT
              ucdmint.sourcekey as SisIntId,
              ucdmext.sourcekey as SisExtId,
              OrganizationCalendarSession.OrganizationCalendarSessionId as TermId,
              RefTermType.Code as TermType,
              RefSessionType.Code as SessionType,
              OrganizationCalendarSession.SessionName as SessionName,
              OrganizationCalendarSession.BeginDate as TermBeginDate,
              OrganizationCalendarSession.EndDate as TermEndDate,
              OrganizationCalendarSession.FirstInstructionDate as InstrBeginDate,
              OrganizationCalendarSession.LastInstructionDate as InstrEndDate
            FROM OrganizationCalendarSession
              LEFT JOIN RefSessionType on RefSessionType.RefSessionTypeId=OrganizationCalendarSession.RefSessionTypeId
              LEFT JOIN OrganizationCalendar on OrganizationCalendar.OrganizationCalendarId=OrganizationCalendarSession.OrganizationCalendarId
              LEFT JOIN RefTermType on OrganizationCalendar.RefTermTypeId=RefTermType.RefTermTypeId
              LEFT JOIN ucdmentitykeymap ucdmint on ucdmint.ucdmkey = OrganizationCalendarSession.OrganizationCalendarSessionId and ucdmint.ucdmentityid = 3 and ucdmint.systemprovisioningid = 1000
              LEFT JOIN ucdmentitykeymap ucdmext on ucdmext.ucdmkey = OrganizationCalendarSession.OrganizationCalendarSessionId and ucdmext.ucdmentityid = 3 and ucdmext.systemprovisioningid = 1001

  """},
  #PersonId,SectionId,Role,RoleStatus,EntryDate,ExitDate,CreditsTaken,CreditsEarned
  'course_section_enrollment' : {
    'index' : 'personid',
    'sis_file' : '{date}%2FCourse_Section_Enrollment_{date}.csv',
    'query' : """
            SELECT
              OrganizationPersonRole.PersonId as PersonId,
              OrganizationPersonRole.OrganizationId as SectionId,
              Role.Name as Role,
              RefRoleStatus.Description as RoleStatus,
              OrganizationPersonRole.EntryDate as EntryDate,
              OrganizationPersonRole.ExitDate as ExitDate,
              PsStudentSection.NumberOfCreditsTaken as CreditsTaken,
              PsStudentSection.NumberOfCreditsEarned as CreditsEarned,
              -- Completed at??
              -- RefWorkflowState.Description as WorkflowState
              'TODO' as WorkflowState
              -- Self-enrolled?
            FROM OrganizationPersonRole
              INNER JOIN Role on Role.RoleId=OrganizationPersonRole.RoleId
              INNER JOIN RoleStatus on RoleStatus.OrganizationPersonRoleId=OrganizationPersonRole.OrganizationPersonRoleId
              INNER JOIN RefRoleStatus on RefRoleStatus.RefRoleStatusId=RoleStatus.RefRoleStatusId
              INNER JOIN PsStudentSection on PsStudentSection.OrganizationPersonRoleId=OrganizationPersonRole.OrganizationPersonRoleId
              -- INNER JOIN RefWorkflowState on RefWorkflowState.RefWorkflowStateId=OrganizationPersonRole.RefWorkflowStateId
  """},
}