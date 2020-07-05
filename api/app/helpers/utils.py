import json
from decimal import *
from datetime import datetime, date
from dateutil import parser

import_field = {
    "Agencia": "agency",
    "Tipo_Identificacion": "identification_type",
    "Nro_Identificacion": "identification_number",
    "Aportes": "contributions",
    "Primer_Nombre": "first_name",
    "Segundo_Nombre": "middle_name",
    "Primer_Apellido": "first_last_name",
    "Segundo_Apellido": "second_last_name",
    "Nombre_Completo": "full_name",
    "Genero": "gender",
    "Fecha_Nacimiento": "date_of_birth",
    "Edad": "age",
    "Nacionalidad": "nationality",
    "Tipo_Persona": "type_person",
    "Vinculo": "link",
    "Estrato": "stratum",
    "Direccion_Residencia": "residence_address",
    "Telefono_Residencia": "residence_phone",
    "Lugar_Residencia": "residence_city",
    "Codigo_CIIUU_Ciudad": "CIIUU_city_code",
    "Celular": "cellphone",
    "Direccion_Comercial": "commercial_address",
    "Telefono_Comercial": "commercial_phone",
    "Lugar_Comercial": "commercial_city",
    "Estado_Civil": "civil_status",
    "Nro_Hijos": "children_number",
    "Personas_a_Cargo": "people_in_charge",
    "Nivel_Estudio": "study_level",
    "Titulo_Graduado": "graduation_title",
    "Titulo_Maximo": "max_title",
    "Profesion": "profession",
    "Empresa_Cargo": "job_position",
    "Empresa_Labora": "company",
    "Estado_Laboral": "labor_status",
    "Empresa_Tipo_contrato": "contract_type",
    "Empresa_Salario": "wage",
    "Ocupacion": "occupation",
    "Acta_Economica": "economic_act",
    "Fecha_Ingreso": "date_of_entry",
    "Fecha_Retiro": "withdrawal_date",
    "Nro_Acta_Ingreso": "entry_certificate_number",
    "Nro_Acta_Retiro": "withdrawal_certificate_number",
    "Numero_Cliente": "client_number",
    "Beneficiario": "beneficiary",
    "Tiene_Inmueble": "have_a_property",
    "Tiene_Vehiculo": "have_a_vehicle",
    "Dependencia": "dependency",
    "Tipo_Vinculo": "type_relationship",
    "Persona_Publicamente_Expuesta": "publicly_exposed_person",
    "Curso_8_Horas": "course_8_hours",
    "Curso_20_Horas": "course_20_hours",
    "Pagaduria": "payroll",
    "Vinculado": "linked",
    "Usuario_Retiro": "user_withdrawal",
    "Fecha_Vinculacion": "date_link",
    "Motivo_Retiro": "withdrawal_reason",
    "Codigo_CIIU_Asociado": "associate_CIIU_code",
    "Total_Ingresos": "total_income",
    "Otros_Ingresos": "others_income",
    "Total_Egresos": "total_expenses",
    "Total_Activos": "total_actives",
    "Total_Pasivo": "total_liabilities",
    "Total_Patrimonio": "total_equity",
    "Descripcion_Otros_Ingresos": "description_others_income",
    "Acta_Reingreso1": "re-entry_act1",
    "Fecha_Reingreso1": "re-entry_date1",
    "Acta_Reingreso2": "re-entry_act2",
    "Fecha_Reingreso2": "re-entry_date2",
    "Operaciones_Moneda_Extranjera": "operations_foreign_currency",
    "Autoriza_Circulacion_Datos": "authorize_circulation_data",
    "Fecha_Ultima_Actualizacion": "date_last_update",
    "Usuario_Ultima_Actualizacion": "user_last_update",
}

import_field_date = [
    "date_of_birth",
    "date_of_entry",
    "withdrawal_date",
    "date_link",
    "re-entry_date1",
    "re-entry_date2",
    "expiration_date",
    "initial_disbursement_date",
    "appraisal_date",
    "last_payment_date",
    "restructuring_date",
    "date_init",
]

import_field_associated = {
    "TipoIden": "type_identification",
    "NIT": "NIT",
    "CodigoContable": "accounting_code",
    "reestructurado": "restructured",
    "NroCredito": "credit_number",
    "FechaDesembolsoInicial": "initial_disbursement_date",
    "FechaVencimiento": "expiration_date",
    "Morosidad": "late_payment",
    "TipoCuota": "type_fee",
    "AlturaCuota": "height",
    "Amortizacion": "amortization",
    "Modalidad": "modality",
    "TasaIntereNominal": "nominal_interest_rate",
    "TasaInteresEfectiva": "effective_interest_rate",
    "ValorPrestamo": "loan_value",
    "ValorCuotaFija": "fixed_fee_value",
    "SaldoCapital": "capital_balance",
    "SaldoIntereses": "interest_balance",
    "OtrosSaldos": "other_balances",
    "Garantia": "warranty",
    "FechaAvaluo": "appraisal_date",
    "Provision": "provision",
    "ProvisionInteres": "provision_interest",
    "Contingencia": "contingency",
    "ValosCuotasExtra": "extra_fee_value",
    "MesesCuotaExtra": "months_extra_fee",
    "fechaultimopago": "last_payment_date",
    "clasegarantia": "warranty_class",
    "destinocredito": "credit_destination",
    "CodOficina": "office_code",
    "AmortiCapital": "capital_amortization",
    "ValorMora": "moral_value",
    "TipoVivienda": "type_housing",
    "VIS": "vis",
    "RangoTipo": "type_range",
    "EntidadRedescuento": "rediscount_entity",
    "MargenRedescuento": "discount_margin",
    "Subsidio": "subsidy",
    "Desembolso": "disbursement",
    "Moneda": "currency",
    "FechaReestructuracion": "restructuring_date",
    "CategoriaReestr": "category_reestr",
    "AportesSociales": "social_contributions",
    "LineaCredEntidad": "credit_line_entity",
    "NumModificaciones": "num_modifications",
    "Estadocredito": "credit_status",
    "NITPatronal": "employer_NIT",
    "NombrePatronal": "employer_name",
}

import_field_associated_obligations = {
    "Tipo_Obligacion": "obligation_type",
    "Tipo_Iden": "identification_type",
    "NIT": "nit",
    "Cod_Municipio": "city_code",
    "Direccion": "Address",
    "Fecha_DesIni": "date_init",
    "Fecha_Vencimiento": "expiration_date",
    "Valor_Credito": "credit_value",
    "Numero_Credito": "credit_number",
    "Plazo_(en_días)": "deadline",
    "Clase_Garantia": "warranty_class",
    "Valor_Garantia": "warranty_value",
    "Amortizacion_(en_días)": "amortization",
    "Tipo_Cuota": "quota_type",
    "Modalidad": "modality",
    "Tasa_Interes_Efectiva": "effective_interest_rate",
    "Saldo_Capital": "capital_balance",
    "Destino_Credito": "destination_credit",
}

import_field_portfolio = {
    "Tipo_identificacion": "type_identification",
    "Numero_Identificacion": "identification_number",
    "Codigo_contable": "accountant_code",
    "Reestructurado": "restructured",
    "Numero_de_credito": "credit_number",
    "Fecha_de_desembolso_inicial": "start_disbursement_date",
    "Fecha_de_vencimiento": "expiration_date",
    "Morosidad": "delinquency",
    "Tipo_de_cuota": "quota_type",
    "Número_de_cuotas_pagadas": "number_of_fees_paid",
    "Amortización": "amortization",
    "Modalidad": "modality",
    "Tasa_de_interés_nominal_cobrada": "nominal_interest_rate_collected",
    "Tasa_de_interés_efectiva": "effective_interest_rate",
    "Valor_préstamo": "loan_value",
    "Valor_cuota_fija": "fixed_quota_value",
    "Saldo_de_capital": "capital_balance",
    "Saldo_de_intereses": "interest_balance",
    "Otros_saldos": "other_saldos",
    "Garantía": "guarantee",
    "Fecha_último_pago": "last_payment_date",
    "Clase_de_garantía": "warranty_type",
    "Destino_crédito": "credit_fate",
    "Código_oficina": "office_code",
    "AmortiCapital": "amorticapital",
    "ValorMora": "default_value",
}

import_field_puc = {
    "CUENTA": "account",
    "DESCRIPCION DE LA CUENTA": "description",
    "SALDO": "amount",
}


def serialize_dict_and_list(data):
    if isinstance(data, dict) or isinstance(data, list):
        data = json.dumps(data, default=json_serializer)

    return data


def json_serializer(elem):
    if isinstance(elem, date) or isinstance(elem, datetime):
        return elem.__str__()
    elif isinstance(elem, Decimal):
        return int(elem)


def transformation_fields(fields={}):
    for field in list(fields.keys()):
        field_act = field.strip()
        if field_act in import_field:
            field_act = import_field[field_act]

        value_field = fields.pop(field)
        if field_act in import_field_date and value_field:
            value_field = parser.parse(value_field)

        fields[field_act.lower()] = value_field
    return fields


def transformation_fields_associated(fields={}):
    for field in list(fields.keys()):
        field_act = field.strip()
        if field_act in import_field_associated:
            field_act = import_field_associated[field_act]

        value_field = fields.pop(field)
        if field_act in import_field_date and value_field:
            value_field = parser.parse(value_field)

        fields[field_act.lower()] = value_field
    return fields


def transformation_fields_puc(fields={}):

    for field in list(fields.keys()):
        field_act = field.strip()
        if field_act in import_field_puc:
            field_act = import_field_puc[field_act]

        value_field = fields.pop(field)
        if field_act in import_field_date and value_field:
            value_field = parser.parse(value_field)

        fields[field_act.lower()] = value_field
    return fields


def transformation_fields_associated_obligations(fields={}):

    for field in list(fields.keys()):
        field_act = field.strip()
        if field_act in import_field_associated_obligations:
            field_act = import_field_associated_obligations[field_act]

        value_field = fields.pop(field)
        if field_act in import_field_date and value_field:
            value_field = parser.parse(value_field, dayfirst=True)

        fields[field_act.lower()] = value_field
    return fields


def transformation_fields_portfolio(fields={}):

    for field in list(fields.keys()):
        field_act = field.strip()
        if field_act in import_field_portfolio:
            field_act = import_field_portfolio[field_act]

        value_field = fields.pop(field)
        if field_act in import_field_date and value_field:
            value_field = parser.parse(value_field, dayfirst=True)

        fields[field_act.lower()] = value_field
    return fields


def days_between(d1, d2):
    return abs((d2 - d1).days)


def list_chunk(info=[], size=50):
    if not bool(info):
        raise Exception("The list of messages comes empty.")

    return [info[i : i + size] for i in range(0, len(info), size)]
