use iso3166::{Country, LIST};

use core::mem;
use std::collections::HashSet;

#[test]
fn should_be_valid() {
    assert_eq!(mem::size_of::<Country>(), mem::size_of::<usize>());

    let mut countries = HashSet::new();
    let mut ids = HashSet::new();
    let mut name = HashSet::new();
    let mut alpha3 = HashSet::new();
    let mut alpha2 = HashSet::new();
    for country in LIST {
        assert!(countries.insert(country));
        assert!(ids.insert(country.id));
        assert!(name.insert(country.name));
        assert!(alpha3.insert(country.alpha3));
        assert!(alpha2.insert(country.alpha2));

        assert_eq!(country, Country::from_alpha2(country.alpha2).unwrap());
        assert!(Country::from_alpha2(&country.alpha2.to_lowercase()).is_none());
        assert_eq!(country, Country::from_alpha2_ignore_case(country.alpha2).unwrap());
        assert_eq!(country, Country::from_alpha2_ignore_case(&country.alpha2.to_lowercase()).unwrap());

        assert_eq!(country, Country::from_alpha3(country.alpha3).unwrap());
        assert!(Country::from_alpha3(&country.alpha3.to_lowercase()).is_none());
        assert_eq!(country, Country::from_alpha3_ignore_case(country.alpha3).unwrap());
        assert_eq!(country, Country::from_alpha3_ignore_case(&country.alpha3.to_lowercase()).unwrap());
    }
}
