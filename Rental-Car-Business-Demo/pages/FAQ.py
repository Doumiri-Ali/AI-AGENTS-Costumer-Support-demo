import streamlit as st

st.title("Frequently Asked Questions (FAQ)")

faqs = {
    "What do I need to rent a car?": (
        "To rent a car, you will need:\n"
        "- A valid driver's license with a minimum of one year of driving experience.\n"
        "- A credit card in your name for the security deposit and payment.\n"
        "- Proof of insurance or an optional insurance coverage offered by the rental company.\n"
        "- In some cases, an additional form of identification, such as a passport or utility bill, may be required."
    ),
    "How old do I need to be to rent a car?": (
        "The minimum age to rent a car is typically 21 years old. However, drivers under 25 may incur a young driver surcharge. "
        "Some rental locations may have a higher minimum age requirement or additional restrictions."
    ),
    "What types of vehicles are available for rent?": (
        "Our rental fleet includes:\n"
        "- **Economy Cars**: Compact and fuel-efficient vehicles perfect for city driving.\n"
        "- **Sedans**: Comfortable cars with more space for passengers and luggage.\n"
        "- **SUVs**: Vehicles with extra cargo space and better handling for off-road conditions.\n"
        "- **Luxury Cars**: High-end vehicles for a premium driving experience.\n"
        "- **Vans**: Spacious options for larger groups or families.\n"
        "- **Convertibles**: Stylish cars with retractable roofs for a fun driving experience."
    ),
    "Can I modify or cancel my reservation?": (
        "Yes, you can modify or cancel your reservation. However, please note the following rules:\n"
        "- **Cancellation**: You can cancel your reservation up to 24 hours before the scheduled pickup time without incurring a cancellation fee. "
        "Cancellations made within 24 hours of pickup may incur a fee equivalent to one day's rental.\n"
        "- **Confirmed Bookings**: Once a booking is confirmed and the start date has passed, you cannot cancel the reservation or receive a refund. "
        "Changes to the booking are not allowed on the start date.\n"
        "- **Modifications**: Changes to the reservation, such as extending the rental period or altering the pickup location, are subject to availability and may incur additional charges."
    ),
    "What is included in the rental price?": (
        "The rental price typically includes:\n"
        "- Basic vehicle rental charges.\n"
        "- Standard mileage allowance (if applicable).\n"
        "- Basic insurance coverage.\n\n"
        "Additional costs such as extra mileage, GPS navigation, child seats, or additional insurance coverage will be billed separately."
    ),
    "What should I do if I have an accident or breakdown?": (
        "In the event of an accident or breakdown:\n"
        "1. Ensure your safety and that of others involved.\n"
        "2. Contact local emergency services if needed.\n"
        "3. Report the incident to our customer service team as soon as possible.\n"
        "4. Follow the instructions provided for towing or vehicle replacement.\n"
        "5. Complete an accident report form if required."
    ),
    "Are there any additional fees or charges?": (
        "Additional fees may include:\n"
        "- **Young Driver Surcharge**: For drivers under 25.\n"
        "- **Additional Driver Fee**: For adding extra drivers to the rental agreement.\n"
        "- **Late Return Fee**: For returning the vehicle later than the agreed-upon time.\n"
        "- **Fuel Charges**: If the vehicle is not returned with a full tank of gas.\n"
        "- **Cleaning Fee**: For excessively dirty vehicles."
    ),
    "Can I return the car to a different location?": (
        "Yes, you can return the car to a different location, but this may incur an additional one-way rental fee. "
        "Please inform us of the drop-off location when making your reservation or contact our customer service to confirm availability."
    ),
    "How is the fuel policy handled?": (
        "Our standard fuel policy requires you to return the vehicle with a full tank of gas. "
        "If the vehicle is returned with less fuel, you will be charged for the missing fuel plus a service fee."
    ),
    "What should I do if I forget personal items in the car?": (
        "If you leave personal items in the car, please contact our customer service as soon as possible. We will make every effort to retrieve your belongings. "
        "Items left in the vehicle will be stored for a limited period before being disposed of according to our lost and found policy."
    ),
    "Can I extend my rental period?": (
        "Yes, you can extend your rental period. Please contact us as soon as possible to arrange for an extension. Extension rates will be based on availability and current rental rates."
    ),
    "Do you offer rental insurance?": (
        "Yes, we offer several insurance options, including:\n"
        "- **Collision Damage Waiver (CDW)**: Reduces your liability in case of damage to the vehicle.\n"
        "- **Supplemental Liability Insurance (SLI)**: Provides additional coverage for third-party claims.\n"
        "- **Personal Accident Insurance (PAI)**: Covers medical expenses for injuries sustained during the rental period.\n\n"
        "You may also use your personal insurance or credit card coverage, but please verify with your provider before making a decision."
    ),
    "What if I need to contact customer support?": (
        "You can reach our customer support team through:\n"
        "- **Phone**: Call our 24/7 customer service number.\n"
        "- **Email**: Send your inquiry to our support email address.\n"
        "- **Online Chat**: Use the live chat feature on our website.\n"
        "- **In-Person**: Visit any of our rental locations for assistance."
    ),
    "What are the rules for reservation and payment?": (
        "Reservations must be made at least 48 hours in advance. Payment is required at the time of booking. "
        "The rental fee will be charged to your credit card, and a security deposit will be held until the vehicle is returned in good condition. "
        "Any damage or additional charges incurred during the rental period will be deducted from the security deposit."
    ),
    "Are there restrictions on the rental period?": (
        "The minimum rental period is 24 hours. For rentals exceeding 30 days, please contact us for special rates. "
        "Extended rentals are subject to approval and may require additional documentation."
    ),
    "What happens if I return the car late?": (
        "If you return the car later than the agreed-upon time, you will incur a late return fee. "
        "The fee is calculated on an hourly basis up to a maximum of one additional day's rental. After that, a full day's rental rate will be charged for each additional day."
    ),
    "Can I cancel a confirmed booking on the start date?": (
        "Once a booking is confirmed and the start date has passed, you cannot cancel the reservation or receive a refund. "
        "No changes or cancellations are allowed on the start date or after the rental period has begun."
    ),
    "Are there any penalties for early return?": (
        "If you return the car earlier than the agreed-upon return date, there will be no refund for unused days. "
        "However, in some cases, an early return may result in a recalculated rental rate, which could be higher than the original rate."
    )
}

# Display each FAQ item
for question, answer in faqs.items():
    st.subheader(question)
    st.markdown(answer)
